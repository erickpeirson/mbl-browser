from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from browser.models import *
from django.conf import settings


def get_base_context():
    return { 'git_revision': settings.GIT_REVISION, }

def get_paginator(model, request, order_by=None, pagesize=25):
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
    return render(request, "browser/base.html")


def course(request, course_id=None):
    context = get_base_context()
    if course_id:
        context['course'] = get_object_or_404(Course, pk=course_id)
        template = "browser/course.html"
    else:
        context['courses'] = get_paginator(Course, request)
        template = "browser/course_list.html"
    return render(request, template, context)


def coursegroup(request, coursegroup_id=None):
    context = get_base_context()
    if coursegroup_id:
        context['coursegroup'] = get_object_or_404(CourseGroup, pk=coursegroup_id)
        template = "browser/coursegroup.html"
    else:

        coursegroups = get_paginator(CourseGroup, request)
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
    context = get_base_context()
    if person_id:
        context['person'] = get_object_or_404(Person, pk=person_id)
        template = "browser/person.html"
    else:
        context['persons'] = get_paginator(Person, request, 'last_name', 100)
        template = "browser/person_list.html"
    return render(request, template, context)


def goals(request):
    return render(request, "browser/goals.html", get_base_context())

def people(request):
    return render(request, "browser/people.html", get_base_context())

def methods(request):
    return render(request, "browser/methods.html", get_base_context())
