from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from browser.models import *
from browser.filters import *



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
    context = RequestContext(request, {})
    if course_id:
        context['course'] = get_object_or_404(Course, pk=course_id)
        template = "browser/course.html"
    else:
        context['courses'] = CourseFilter(request.GET, queryset=Course.objects.order_by('year'))
        template = "browser/course_list.html"
    return render(request, template, context)


def coursegroup(request, coursegroup_id=None):
    """
    Handles both list and detail views for :class:`.CourseGroup`\s.
    """
    context = RequestContext(request, {})
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
    context = RequestContext(request, {})
    if person_id:
        person = get_object_or_404(Person, pk=person_id)
        context.update({
            'person': person,
            # 'affiliated_with': affiliated_with(person),
        })
        template = "browser/person.html"
    else:
        context['persons'] = PersonFilter(request.GET, queryset=Person.objects.order_by('last_name'))
        # context['persons'] = get_paginator(Person, request, 'last_name', 100)
        template = "browser/person_list.html"
    return render(request, template, context)


def institution(request, institution_id=None):
    """
    Handles both list and detail views for :class:`.Person`\s.
    """
    context = RequestContext(request, {})
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


def goals(request):
    return render(request, "browser/goals.html", RequestContext(request, {}))

def people(request):
    return render(request, "browser/people.html", RequestContext(request, {}))

def methods(request):
    return render(request, "browser/methods.html", RequestContext(request, {}))
