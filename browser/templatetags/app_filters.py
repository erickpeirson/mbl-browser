from django.template import Library
from browser.models import *

from collections import defaultdict

register = Library()


@register.filter(name="get_range")
def get_range(value, offset=0):
    return range(offset, value+offset)


@register.filter
def get_years(coursegroup):
    years = [ p.year for p in coursegroup.partof_set.all()]
    if min(years) == max(years):
        return u'{year}'.format(year=min(years))
    return u'{min} to {max}'.format(min=min(years), max=max(years))


@register.filter
def get_attendance(instance):
    """
    Retrieve :class:`.Attendance` instances associated with a ``course``.

    Results are ordered by role.
    """
    if type(instance) is Course:
        return instance.attendance_set.distinct('role', 'person_id').order_by('role', 'person_id')
    elif type(instance) is Person:
        return instance.attendance_set.distinct('year', 'role', 'course_id').order_by('year', 'role', 'course_id')


@register.filter
def get_affiliation(person, year):
    """
    Get all unique :class:`.Affiliation` instances for ``person`` in ``year``.
    """
    return person.affiliation_set.filter(year=year).distinct('institution_id')


@register.filter
def get_affiliations(person):
    return person.affiliation_set.distinct('year', 'institution_id').order_by('year')


@register.filter
def get_location(person, year):
    """
    Get all unique :class:`.Localization` isntances for ``person`` in ``year``.
    """
    return person.localization_set.filter(year=year).distinct()


@register.filter
def get_localizations(person):
    return person.localization_set.distinct('year', 'location_id').order_by('year', 'location_id')


@register.filter
def get_denizens(location):
    return location.localization_set.distinct('year', 'person_id').order_by('year', 'person_id')


@register.filter
def get_locations(person):
    return person.locations.distinct('id')


@register.filter
def get_affiliation_count(course):
    """
    Calculate the number of :class:`.Institution`\s associated with a
    ``course``.
    """

    return Affiliation.objects.filter(
            person__in=course.attendees.distinct('id')
        ).filter(
            year=course.year
        ).distinct(
            'institution_id'
        ).count()


@register.filter
def get_coursegroup_attendance_count(coursegroup):
    """
    Calculate the total number of attendees across all :class:`.Course`\s
    that are part of ``coursegroup``.

    TODO: This should count _unique_ people, not sum the course attendance
    counts.
    """
    return Attendance.objects.filter(course__in=coursegroup.courses.all()).distinct('person').count()


@register.filter
def get_coursegroup_attendance(coursegroup):
    return Attendance.objects.filter(course__in=coursegroup.courses.all())


@register.filter
def get_coursegroup_attendees(coursegroup):
    return Person.objects.filter(attendance_set__in=get_coursegroup_attendance(coursegroup)).distinct('id')


@register.filter
def get_coursegroup_affiliation_count(coursegroup):
    return Affiliation.objects.filter(person__in=get_coursegroup_attendees(coursegroup))


@register.filter
def get_partof_set(coursegroup):
    return coursegroup.partof_set.distinct('year', 'course_id').order_by('year', 'course_id')


@register.filter
def get_researches(person):
    return Investigator.objects.filter(person=person).distinct('year', 'id').order_by('year', 'id')


@register.filter
def get_affiliates(institution):
    afields = ['person_id', 'year', 'position']
    aqs = Affiliation.objects.filter(institution_id=institution.id)\
                             .distinct(*afields)

    person_affiliations = defaultdict(list)
    for affiliation in aqs.values(*afields):
        person_affiliations[affiliation['person_id']].append(affiliation)

    pfields = ['last_name', 'first_name', 'pk']
    qs = []
    for person in institution.affiliates.distinct('pk').values(*pfields):
        person['positions'] = person_affiliations[person['pk']]
        qs.append(person)

    # HyperlinkedIdentityField requires the HttpRequest to generate an
    #  absolute URL.

    return qs


@register.filter
def get_positions(person):
    return Position.objects.filter(person=person).order_by('year')


@register.simple_tag
def get_roles_of_positions():
    list_of_roles = []
    for i in Position.role_choices:
        list_of_roles.append(i[1])
    return list_of_roles
