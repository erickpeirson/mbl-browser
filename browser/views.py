from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models.query_utils import Q
from django.db.models import Count

from browser.models import *
from browser.filters import *

from itertools import chain, groupby



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
