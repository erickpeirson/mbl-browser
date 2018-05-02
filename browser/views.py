from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models.query_utils import Q
from django.db.models import Count
from django.db import transaction
from django.contrib import messages

from browser.models import *
from browser.filters import *
from browser.forms import *

from itertools import chain, groupby
import datetime


def get_paginator(model, request, order_by=None, pagesize=25):
    """
    Generic paginator functionality for views.
    """
    queryset = model.objects.all()
    if order_by:
        queryset = queryset.order_by(order_by)
    paginator = Paginator(queryset, pagesize)
    page = request.GET.get('page')
    try:
        instances = paginator.page(page)
    except PageNotAnInteger:
        instances = paginator.page(1)
    except EmptyPage:
        instances = paginator.page(paginator.num_pages)
    return instances


def home(request):
    """
    The view at /.
    """
    return render(request, "browser/base.html")


def course(request, course_id=None):
    """
    Handles both list and detail views for :class:`.Course`\s.
    """
    context = {}
    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        context.update({
            'course': course,
        })
        template = "browser/course.html"
    else:
        context['courses'] = CourseFilter(request.GET, queryset=Course.objects.order_by('year'))
        template = "browser/course_list.html"
    return render(request, template, context)


def coursegroup(request, coursegroup_id=None):
    """
    Handles both list and detail views for :class:`.CourseGroup`\s.
    """
    context = {}
    if coursegroup_id:
        context['coursegroup'] = get_object_or_404(CourseGroup, pk=coursegroup_id)
        template = "browser/coursegroup.html"
    else:
        # coursegroups = get_paginator(CourseGroup, request, order_by='name')
        coursegroups = CourseGroupFilter(request.GET, queryset=CourseGroup.objects.all())
        context['coursegroups'] = coursegroups
        template = "browser/coursegroup_list.html"
    return render(request, template, context)


def coursegroup_data(request, coursegroup_id=None):
    if coursegroup_id:
        coursegroup = get_object_or_404(CourseGroup, pk=coursegroup_id)

    data = [{
        'id': partof.course.id,
        'year': partof.year,
        'attendees': partof.course.attendance_set.distinct('role', 'person_id').order_by('role', 'person_id').count()
    } for partof in coursegroup.partof_set.all()]
    return JsonResponse({'attendance': data})


def person(request, person_id=None):
    """
    Handles both list and detail views for :class:`.Person`\s.
    """
    context = {}
    if person_id:
        person = get_object_or_404(Person, pk=person_id)
        context.update({
            'person': person,
            # 'affiliated_with': affiliated_with(person),
        })
        template = "browser/person.html"
    else:
        context['persons'] = PersonFilter(request.GET, queryset=Person.objects.order_by('last_name').filter(merge_from=None))
        # context['persons'] = get_paginator(Person, request, 'last_name', 100)
        template = "browser/person_list.html"

    return render(request, template, context)


def institution(request, institution_id=None):
    """
    Handles both list and detail views for :class:`.Person`\s.
    """
    context = {}
    if institution_id:
        institution = get_object_or_404(Institution, pk=institution_id)
        context.update({
            'institution': institution,
        })
        template = "browser/institution.html"
    else:
        context['institutions'] = InstitutionFilter(request.GET, queryset=Institution.objects.order_by('name'))
        template = "browser/institution_list.html"
    return render(request, template, context)


def location(request, location_id=None):
    """
    Handles both list and detail views for :class:`.Location`\s.
    """
    context = {}
    if location_id:
        location = get_object_or_404(Location, pk=location_id)
        context.update({
            'location': location,
        })
        template = "browser/location.html"
    else:
        context['locations'] = LocationFilter(request.GET, queryset=Location.objects.order_by('name'))
        template = "browser/location_list.html"
    return render(request, template, context)


def goals(request):
    return render(request, "browser/goals.html", {})

def about(request):
    return render(request, "browser/about.html", {})

def methods(request):
    return render(request, "browser/methods.html", {})


def generic_autocomplete(request):
    """
    A quick-and-dirty autocomplete for the front page.
    """
    query = request.GET.get('query', None)

    models = [
        (Person, ['last_name', 'first_name']),
        (CourseGroup, ['name']),
        (Institution, ['name']),
    ]
    results = []
    if query and len(query) > 2:
        query_parts = query.split(' ')

        for model, fields in models:
            qs = model.objects.all()
            resultset = []

            for field in fields:
                for part in query_parts:
                    if len(part) < 3:
                        continue
                    resultset = chain(resultset, qs.filter(**{'%s__icontains' % field: part}).values('id', *fields))
                    # q |= Q(**{'%s__istartswith' % field: part})
            grouped = [(i, [o for o in objects]) for i, objects in groupby(sorted(resultset, key=lambda o: o['id']), key=lambda o: o['id'])]
            for i, objects in sorted(grouped, key=lambda o: len(o[1]))[::-1]:
            # for obj in model.objects.filter(q):
                obj = objects[0]

                results.append({
                    'model': model.__name__,
                    'url': reverse(model.__name__.lower(), args=[obj['id']]),
                    'name': obj.get('name', '%s %s' % (obj.get('first_name'), obj.get('last_name'))),
                })
                if len(results) > 20:
                    break

            if len(results) > 20:
                break
    return JsonResponse({'results': results})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', reverse('home')))


def _handle_known_person_form(request, extra_form, person):
    known_person = extra_form.save(commit=False)
    existing = None
    if known_person.conceptpower_uri:
        try:
            existing = KnownPerson.objects.get(conceptpower_uri=known_person.conceptpower_uri)
        except KnownPerson.DoesNotExist:
            existing = None

    if existing:
        person.authority = existing
        person.save()
    elif known_person.conceptpower_uri:
        if getattr(known_person, 'changed_by', None) is None:
            known_person.changed_by = request.user
        known_person.save()
        person.authority = known_person
        person.save()


@staff_member_required
def handle_person(request, person_id=None):
    template = "browser/change_person.html"
    context = {}
    person = None

    if person_id:
        person = get_object_or_404(Person, pk=person_id)

    if request.method == 'GET':
        if person_id:
            form = PersonForm(instance=person)
            extra_form = KnownPersonForm(instance=person.authority, prefix='known')
        else:
            form = PersonForm(initial={'changed_by': request.user})
            extra_form = KnownPersonForm()

    if request.method == 'POST':
        if person_id:
            form = PersonForm(request.POST, instance=person)
            extra_form = KnownPersonForm(request.POST, instance=person.authority, prefix='known')
        else:
            form = PersonForm(request.POST)
            extra_form = KnownPersonForm(request.POST)

        if form.is_valid():
            form.cleaned_data["changed_by"] = request.user
            person = form.save()
        else:
            # Return to change_person.html if form is invalid
            context.update({
                'form': form,
                'person': person,
                'extra_form': extra_form
            })
            return render(request, template, context)

        if person.validated and person.validated_by is None:
            person.validated_by = request.user
            person.validated_on = datetime.datetime.now()
            person.save()

        if extra_form.is_valid():
            _handle_known_person_form(request, extra_form, person)
        return HttpResponseRedirect(reverse('person', args=(person.id,)))

    context.update({
        'form': form,
        'person': person,
        'extra_form': extra_form
    })
    return render(request, template, context)


@staff_member_required
def edit_institution(request, institution_id):
    institution = get_object_or_404(Institution, pk=institution_id)
    if request.method == 'GET':
        form = InstitutionForm(instance=institution)
    elif request.method == 'POST':
        form = InstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            institution = form.save()
            if institution.validated and institution.validated_by is None:
                institution.validated_by = request.user
                institution.validated_on = datetime.datetime.now()
                institution.save()
            return HttpResponseRedirect(reverse('institution', args=(institution.id,)))
    context = {
        'form': form,
        'institution': institution,
    }

    template = "browser/change_base.html"
    return render(request, template, context)


@staff_member_required
def edit_coursegroup(request, coursegroup_id):
    coursegroup = get_object_or_404(CourseGroup, pk=coursegroup_id)
    if request.method == 'GET':
        form = CourseGroupForm(instance=coursegroup)
    elif request.method == 'POST':
        form = CourseGroupForm(request.POST, instance=coursegroup)
        if form.is_valid():
            coursegroup = form.save()
            if coursegroup.validated and coursegroup.validated_by is None:
                coursegroup.validated_by = request.user
                coursegroup.validated_on = datetime.datetime.now()
                coursegroup.save()
            return HttpResponseRedirect(reverse('coursegroup', args=(coursegroup.id,)))
    context = {
        'form': form,
        'coursegroup': coursegroup,
    }

    template = "browser/change_base.html"
    return render(request, template, context)


@staff_member_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'GET':
        form = CourseForm(instance=course)
    elif request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            if course.validated and course.validated_by is None:
                course.validated_by = request.user
                course.validated_on = datetime.datetime.now()
                course.save()
            return HttpResponseRedirect(reverse('course', args=(course.id,)))
    context = {
        'form': form,
        'course': course,
    }

    template = "browser/change_course.html"
    return render(request, template, context)


def _handle_known_location_form(request, extra_form, location):
    known_location = extra_form.save(commit=False)
    existing = None
    if known_location.external_uri:
        try:
            existing = KnownLocation.objects.get(external_uri=known_location.external_uri)
        except KnownLocation.DoesNotExist:
            existing = None
    if not existing and known_location.geo_uri:
        try:
            existing = KnownLocation.objects.get(geo_uri=known_location.geo_uri)
        except KnownLocation.DoesNotExist:
            existing = None
    if existing:
        location.authority = existing
        location.save()
    elif known_location.geo_uri or known_location.external_uri:
        if getattr(known_location, 'changed_by', None) is None:
            known_location.changed_by = request.user
        known_location.save()
        location.authority = known_location
        location.save()


@staff_member_required
def edit_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.method == 'GET':
        form = LocationForm(instance=location)
        extra_form = KnownLocationForm(instance=location.authority, prefix='known')
    elif request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        extra_form = KnownLocationForm(request.POST, instance=location.authority, prefix='known')
        if form.is_valid():
            location = form.save()
            if location.validated and location.validated_by is None:
                location.validated_by = request.user
                location.validated_on = datetime.datetime.now()
                location.save()

            if extra_form.is_valid():
                _handle_known_location_form(request, extra_form, location)
            return HttpResponseRedirect(reverse('location', args=(location.id,)))
    context = {
        'form': form,
        'extra_form': extra_form,
        'location': location,
    }

    template = "browser/change_location.html"
    return render(request, template, context)


@staff_member_required
def split_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'GET':
        form = SplitPersonForm(initial={
            'last_name': person.last_name,
            'first_name': person.first_name
        }, person=person)


    elif request.method == 'POST':
        form = SplitPersonForm(request.POST, person=person)
        if form.is_valid():
            new_person = form.save(request.user)
            return HttpResponseRedirect(reverse('person', args=(new_person.id,)))

    context = {
        'form': form,
        'person': person,
    }

    template = "browser/split_person.html"
    return render(request, template, context)


@staff_member_required
def split_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    if request.method == 'GET':
        form = SplitLocationForm(initial={
            'name': location.name,
        }, location=location)
        extra_form = KnownLocationForm(instance=location.authority, prefix='known')

    elif request.method == 'POST':
        form = SplitLocationForm(request.POST, location=location)
        extra_form = KnownLocationForm(request.POST, instance=location.authority, prefix='known')
        if form.is_valid():
            new_location = form.save(request.user)
            if extra_form.is_valid():
                _handle_known_location_form(request, extra_form, location)
            return HttpResponseRedirect(reverse('location', args=(new_location.id,)))

    context = {
        'form': form,
        'location': location,
        'extra_form': extra_form,
    }

    template = "browser/split_location.html"
    return render(request, template, context)


@staff_member_required
def bulk_action(request, model):
    if request.method == 'POST':
        action = request.POST.get('action')
        instance_ids = request.POST.getlist('action_select')
        model_name = request.POST.get('model')
        if model_name == 'person':
            if action == 'merge':
                return merge_people(request, instance_ids)
        elif model_name == 'location':
            if action == 'merge':
                return merge_locations(request, instance_ids)


@staff_member_required
def merge_people(request, person_ids):
    perform = request.POST.get('perform', False)
    context = {}
    if perform:
        form = MergePersonForm(request.POST, people=person_ids)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('person', args=(form.cleaned_data.get('merge_into').id,)))
    else:
        form = MergePersonForm(people=person_ids)

    context.update({
        'form': form,
        'people': Person.objects.filter(pk__in=person_ids)
    })

    template = "browser/merge_people.html"
    return render(request, template, context)


@staff_member_required
def merge_locations(request, location_ids):
    perform = request.POST.get('perform', False)
    context = {}
    if perform:
        form = MergeLocationForm(request.POST, locations=location_ids)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('location', args=(form.cleaned_data.get('merge_into').id,)))
    else:
        form = MergeLocationForm(locations=location_ids)

    context.update({
        'form': form,
        'locations': Location.objects.filter(pk__in=location_ids)
    })

    template = "browser/merge_locations.html"
    return render(request, template, context)


@staff_member_required
def course_create(request, coursegroup_id=None):
    """
    Allows a curator to create a new course record as part of a course group.
    """
    context = {}
    if coursegroup_id is None:
        template = 'browser/course_create_choose_group.html'
        if request.method == 'GET':
            form = GroupForCourseForm()
        elif request.method == 'POST':
            form = GroupForCourseForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data.get('group')
                print form.cleaned_data
                create_group = form.cleaned_data.get('group_create', False)
                group_name = form.cleaned_data.get('group_name')
                if create_group and group_name:
                    group = CourseGroup.objects.create(name=group_name,
                                                       changed_by=request.user)

                return HttpResponseRedirect(reverse('create-course', args=(group.id,)))

    else:
        coursegroup = get_object_or_404(CourseGroup, pk=coursegroup_id)
        template = 'browser/course_create.html'
        if request.method == 'GET':
            form = CourseInstanceForm()
        elif request.method == 'POST':
            form = CourseInstanceForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    course = Course.objects.create(
                        name = form.cleaned_data['name'],
                        validated = form.cleaned_data.get('validated'),
                        year = form.cleaned_data['year'],
                        changed_by = request.user,
                    )
                    partof = PartOf.objects.create(
                        year = form.cleaned_data['year'],
                        course = course,
                        coursegroup = coursegroup,
                        changed_by = request.user,
                    )
                return HttpResponseRedirect(reverse('course', args=(course.id,)))
        context = {'coursegroup': coursegroup,}
    context.update({'form': form})
    return render(request, template, context)


@staff_member_required
def course_delete(request, course_id):
    """
    Allows a curator to delete a course record.
    """
    template = 'browser/course_delete.html'
    confirmed = request.GET.get('confirmed', False)
    next_page = request.GET.get('next', reverse('courses'))
    course = get_object_or_404(Course, pk=course_id)
    context = {}
    if course.can_delete():
        if confirmed:
            course.delete()
            return HttpResponseRedirect(next_page)
    else:
        context.update({'error': True})
    context.update({
        'next_page': next_page,
        'course': course
    })
    return render(request, template, context)


@staff_member_required
def attendee_create(request, course_id):
    """
    Allows a curator to add an attendee to a course.
    """

    course = get_object_or_404(Course, pk=course_id)
    template = 'browser/attendee_create.html'
    if request.method == 'GET':
        form = AttendeeForm()

    elif request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                person = form.cleaned_data.get('person')
                create = form.cleaned_data.get('create_person')
                if create and not person:
                    surname = form.cleaned_data.get('create_person_lastname')
                    forename = form.cleaned_data.get('create_person_firstname')
                    person = Person.objects.create(
                        first_name=forename,
                        last_name=surname,
                        changed_by=request.user
                    )

                attendance = Attendance.objects.create(
                    person = person,
                    year = course.year,
                    course = course,
                    role = form.cleaned_data.get('role'),
                    changed_by=request.user
                )

                location_literal = form.cleaned_data.get('location')
                if location_literal:
                    location = Location.objects.create(
                        name = location_literal,
                        changed_by=request.user
                    )
                    localization = Localization.objects.create(
                        person = person,
                        location = location,
                        year = course.year,
                        changed_by=request.user
                    )

                institution = form.cleaned_data.get('institution')
                institution_name = form.cleaned_data.get('institution_search')
                create_institution = form.cleaned_data.get('create_institution')
                position = form.cleaned_data.get('position')

                if create_institution:
                    institution = Institution.objects.create(
                        name = institution_name,
                        changed_by=request.user
                    )
                affiliation = Affiliation.objects.create(
                    person = person,
                    institution = institution,
                    year = course.year,
                    position = position,
                    changed_by=request.user
                )

            return HttpResponseRedirect(reverse('course', args=(course.id,)))
    context = {
        'course': course,
        'form': form,
    }
    return render(request, template, context)


@staff_member_required
def add_investigator_record(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    template = "browser/investigator.html"
    form = InvestigatorForm()

    if request.method == 'POST':
        form = InvestigatorForm(request.POST, instance=person)
        if form.is_valid():
            investigator = Investigator(subject=form.cleaned_data.get('subject'),
                                            role=form.cleaned_data.get('role'),
                                            person_id=person_id, year=form.cleaned_data.get('year'),
                                            changed_by=request.user)
            investigator.save()
            return HttpResponseRedirect(reverse('person', args=(person.id,)))

    context = {
        'form': form,
        'person': person,
        'type': 'create_investigator'
    }

    return render(request, template, context)


@staff_member_required
def edit_investigator_record(request,person_id,research_id):
    person = get_object_or_404(Person, pk=person_id)
    research = get_object_or_404(Investigator, pk=research_id)
    template = "browser/investigator.html"

    # Retreive investigator data already stored in database and display to the user
    form = InvestigatorForm(initial={'subject': research.subject, 'role': research.role,
                                             'year': research.year})

    if request.method == 'POST':
        form = InvestigatorForm(request.POST, instance=person)
        if form.is_valid():
            research.subject = form.cleaned_data.get('subject')
            research.role = form.cleaned_data.get('role')
            research.year = form.cleaned_data.get('year')
            research.save()
            return HttpResponseRedirect(reverse('person', args=(person.id,)))

    context = {
        'form': form,
        'person': person,
        'investigator_data': research,
        'type': 'edit_investigator'
    }

    return render(request, template, context)


@staff_member_required
def delete_investigator_record(request, person_id, research_id):
    if request.method == 'POST':
        Investigator.objects.filter(id=research_id).delete()

    return HttpResponseRedirect(reverse('person', args=(person_id,)))


@staff_member_required
def edit_affiliation(request, person_id, affiliation_id):
    person = get_object_or_404(Person, pk=person_id)
    affiliation = get_object_or_404(Affiliation, pk=affiliation_id)
    template = "browser/affiliation_edit.html"
    form = EditAffiliationForm(initial={'institution': affiliation.institution,
                                        'position': affiliation.position, 'institution_id': affiliation.institution.id})
    context = {
        'form': form,
        'person': person
    }

    if request.method == 'POST':
        form = EditAffiliationForm(request.POST, instance=person)
        if form.is_valid():
            if form.cleaned_data.get('institution'):
                # If institution_id is not populated then create the institution before updating affiliation
                if not form.cleaned_data.get('institution_id'):
                    # Checking if create institution radio button has been checked
                    if not form.cleaned_data.get('create_institution'):
                        messages.add_message(request, messages.ERROR,
                                             'The above institute does not exist in the database. '
                                             'Please check the checkbox below to create '
                                             'information about the institute.')
                        context.update({'form': form})
                        return render(request, template, context)
                    else:
                        institution = Institution.objects.create(
                            name=form.cleaned_data.get('institution'),
                            changed_by=request.user
                        )
                        form.cleaned_data["institution_id"] = institution.id
            Affiliation.objects.select_related().filter(person_id=affiliation.person_id, year=affiliation.year,
                        institution=affiliation.institution).update(position=form.cleaned_data.get('position'),
                                        institution=Institution.objects.get(id=form.cleaned_data.get('institution_id')))
            return HttpResponseRedirect(reverse('person', args=(person_id,)))

    return render(request, template, context)


@staff_member_required
def position(request, person_id, position_id=None):
    person = get_object_or_404(Person, pk=person_id)
    template = "browser/position.html"

    context = {
        'person': person,
        'position_id': position_id
    }

    if request.method == 'GET':
        if position_id:
            position = get_object_or_404(Position, pk=position_id)
            form = PositionForm(initial={'subject': position.subject, 'role': position.role,
                                         'year': position.year, 'start_date': position.start_date,
                                         'end_date': position.end_date})
        else:
            form = PositionForm()

        context.update({
            'form': form
        })

    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            if position_id is None:
                Position.objects.create(
                    person_id=person_id,
                    changed_by=request.user,
                    **form.cleaned_data
                )
            else:
                Position.objects.filter(id=position_id).update(**form.cleaned_data)
            return HttpResponseRedirect(reverse('person', args=(person.id,),)+'?tab=person-positions')
        context.update({
            'form': form
        })
    return render(request, template, context)


@staff_member_required
def delete_position(request, person_id, position_id):
    if request.method == 'POST':
        Position.objects.filter(id=position_id).delete()
    return HttpResponseRedirect(reverse('person', args=(person_id,)))
