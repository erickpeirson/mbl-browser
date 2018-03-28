from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.conf import settings

from browser.models import *
import csv
import os
import codecs


def isnan(value):
    return str(value) == 'nan' or str(value) == ''

USER_RUNNING_IMPORT = settings.IMPORT_USER

class Command(BaseCommand):
    help = 'Load MBL data from CSV'

    datatypes = [
        ('coursegroup', 'coursegroup.csv'),
        ('institution', 'institution.csv'),
        ('location', 'location.csv'),
        ('course', 'course.csv'),
        ('person', 'person.csv'),
        ('affiliations', 'cleaned_affiliations.csv'),
        ('attendance', 'cleaned_coursedata.csv'),
        ('coursegroups', 'cleaned_coursegroups.csv'),
        ('investigators', 'cleaned_investigators.csv'),
        ('locations', 'cleaned_locations.csv'),
        ('combined_attendances', 'combined_attendances.csv')
    ]

    def add_arguments(self, parser):
        parser.add_argument('datapath', nargs=1, type=str)

    def handle(self, *args, **options):
        path = options['datapath'][0]
        for name, fname in self.datatypes:
            print 'Loading %s from %s' % (name, fname)
            if not os.path.isfile(os.path.join(path, fname)):
                print '[INFO] file %s does not exist.' % (os.path.join(path, fname))
                continue
            method = getattr(self, 'handle_{0}'.format(name))
            for datum in self.load_csv(os.path.join(path, fname)):
                try:
                    method(datum)
                except IntegrityError:
                    pass


    def handle_coursegroup(self, datum):
        instance = CourseGroup(name=datum['Course Group'],
                               uri=datum['Course Group URI'])
        instance.save()

    def handle_institution(self, datum):
        instance = Institution(name=datum['Institution'],
                               uri=datum['Institution URI'])
        instance.save()

    def handle_location(self, datum):
        instance = Location(name=datum['Location'],
                               uri=datum['Location URI'])
        instance.save()

    def handle_course(self, datum):
        instance = Course(name=datum['Course Name'],
                          uri=datum['Course URI'])
        instance.save()

    def handle_person(self, datum):
        try:
            instance = Person(first_name=datum['First Name'],
                              last_name=datum['Last Name'],
                              uri=datum['Person URI'],
                              changed_by=auth.User)
            instance.save()
        except Exception as e:
            print "Error while importing: ", e

    def handle_affiliations(self, datum):
        if isnan(datum['Person URI']) or isnan(datum['Institution URI']):
            return
        person = Person.objects.get(uri=datum['Person URI'])
        institution = Institution.objects.get(uri=datum['Institution URI'])
        instance = Affiliation(person=person,
                               institution=institution,
                               year=datum['Year'],
                               position=datum['Position'])
        instance.save()

    def handle_attendance(self, datum):
        if isnan(datum['Course URI']) or isnan(datum['Person URI']):
            return
        person = Person.objects.get(uri=datum['Person URI'])
        course = Course.objects.get(uri=datum['Course URI'])
        instance = Attendance(person=person,
                              course=course,
                              year=datum['Year'],
                              role=datum['Role'])
        instance.save()

    def handle_coursegroups(self, datum):
        if isnan(datum['Course URI']) or isnan(datum['Course Group URI']):
            return
        course = Course.objects.get(uri=datum['Course URI'])
        coursegroup = CourseGroup.objects.get(uri=datum['Course Group URI'])
        instance = PartOf(course=course,
                          coursegroup=coursegroup,
                          year=datum['Year'])
        instance.save()

    def handle_investigators(self, datum):
        if isnan(datum['Person URI']):
            return
        person = Person.objects.get(uri=datum['Person URI'])
        instance = Investigator(person=person,
                                year=datum['Year'],
                                role=datum['Role'],
                                subject=datum['Subject'])
        instance.save()

    def handle_locations(self, datum):
        if isnan(datum['Person URI']) or isnan(datum['Location URI']):
            return
        person = Person.objects.get(uri=datum['Person URI'])
        location = Location.objects.get(uri=datum['Location URI'])
        instance = Localization(person=person,
                                location=location,
                                year=datum['Year'])
        instance.save()

    def handle_combined_attendances(self, datum):
        # if there is no course uri set, return
        if isnan(datum['Course URI']):
            return

        # find course by id (uris in csv are not real uris)
        course_id = os.path.basename(os.path.normpath(datum['Course URI']))
        try:
            course = Course.objects.get(pk=course_id)
        except:
            print "[ERROR] Course with id %s does not exist." % (course_id)
            return

        person = None
        person_first_name = datum['First Name'].decode('utf-8')
        person_last_name = datum['Last Name'].decode('utf-8')
        person_candidates = Person.objects.filter(last_name__iexact=datum['Last Name'])
        if person_candidates:
            for person_candidate in person_candidates:
                if person_first_name in person_candidate.first_name:
                    person = person_candidate
                    print '[WARNING] It seems like %s %s already exists. Using existing person.' % (person_first_name, person_last_name)
                    break

        # add imported by user
        user = User.objects.get(username=USER_RUNNING_IMPORT)

        # create person
        if not person:
            person = Person(first_name=person_first_name,
                              last_name=person_last_name, changed_by_id=user.pk)
        try:
            person.save()
        except Exception as e:
            print e
            return


        # create affiliation
        institution_name = datum['Institution'].decode('utf-8').strip()
        if institution_name:
            institutions = Institution.objects.filter(name__iexact=institution_name)
            if institutions:
                institution = institutions[0]
                print '[INFO] found %s. Using existing institution.' % (institution_name)
            else:
                institution = Institution(name=institution_name, changed_by_id=user.pk)
                try:
                    institution.save()
                except Exception as e:
                    print e
                    return

            affiliation = Affiliation(person=person,
                                   institution=institution,
                                   year=datum['Year'],
                                   position=datum['Position'], changed_by_id=user.pk)
            try:
                affiliation.save()
            except Exception as e:
                print e
                return

        attendance = Attendance.objects.filter(person=person, course=course)
        if attendance:
            print "[WARNING] person already recorded as attendent of %s. Skipping person." % (course.name)
            return

        # create Attendance
        attendance = Attendance(person=person,
                              course=course,
                              year=datum['Year'],
                              role=datum['Role'], changed_by_id=user.pk)
        try:
            attendance.save()
        except Exception as e:
            print e
            return


    def load_csv(self, path):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
        return data
