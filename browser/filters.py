from builtins import object
import django_filters as df
from django.db.models import Count
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.db.models import Max, Min

#from rest_framework import filters
from django_filters import rest_framework as filters

from browser.models import *


class CBooleanWidget(df.widgets.BooleanWidget):
    """
    Overrides :class:`django_filters.widgets.BooleanWidget` in order to allow
    configuration of the empty option.
    """
    def __init__(self, attrs=None, empty=None):
        choices = (('', _(empty) if empty else _('Unknown')),
                   ('true', _('Yes')),
                   ('false', _('No')))
        super(df.widgets.BooleanWidget, self).__init__(attrs, choices)


class CourseFilter(filters.FilterSet):
    name = df.CharFilter(field_name='name', lookup_expr='icontains',
                         label='Course name')
    occurred_from = df.NumberFilter(field_name='year', lookup_expr='gte',
                                    label='Occurred from')
    occurred_through = df.NumberFilter(field_name='year', lookup_expr='lte',
                                       label='Occurred through')
    last_updated = df.DateTimeFilter(field_name='last_updated', lookup_expr='gte',
                                     label='Last updated')

    o = df.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'), ('last_updated', 'last_updated'),
        ),

        field_labels={
            'name': 'Name', 'last_updated': 'Last updated',
        }
    )

    class Meta(object):
        model = Course
        fields = ['name', 'occurred_from', 'occurred_through',]


class InstitutionFilter(filters.FilterSet):
    name = df.CharFilter(field_name='name', lookup_expr='icontains',
                         label='Institution name')
    last_updated = df.DateTimeFilter(field_name='last_updated', lookup_expr='gte',
                                     label='Last updated')

    o = df.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'), ('last_updated', 'last_updated'),
        ),

        field_labels={
            'name': 'Name', 'last_updated': 'Last updated',
        }
    )

    class Meta(object):
        model = Institution
        fields = ['name', ]


class CourseGroupFilter(filters.FilterSet):
    name = df.CharFilter(field_name='name', lookup_expr='icontains',
                         label='Course name')
    occurred_from = df.NumberFilter(method='filter_occurred_from',
                                    label='Occurred from')
    occurred_through = df.NumberFilter(method='filter_occurred_through',
                                      label='Occurred through')
    last_updated = df.DateTimeFilter(field_name='last_updated', lookup_expr='gte',
                                     label='Last updated')

    o = df.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'), ('last_updated', 'last_updated'),
        ),

        field_labels={
            'name': 'Name', 'last_updated': 'Last updated',
        }
    )

    class Meta(object):
        model = CourseGroup
        fields = ['name', ]


    def filter_occurred_from(self, queryset, name, value):
        if not value:
            return queryset
        queryset = queryset.annotate(latest_course=Max('courses__year'))
        return queryset.filter(latest_course__gte=value)

    def filter_occurred_through(self, queryset, name, value):
        if not value:
            return queryset
        queryset = queryset.annotate(earliest_course=Min('courses__year'))
        return queryset.filter(earliest_course__lte=value)


class PersonFilter(filters.FilterSet):
    name = df.CharFilter(method='filter_name', label='Full name')
    last_name = df.CharFilter(field_name='last_name', lookup_expr='icontains',
                              label='Surname')
    first_name = df.CharFilter(field_name='first_name', lookup_expr='icontains',
                               label='Forename')
    location = df.CharFilter(method='filter_location', label='Location')
    affiliation = df.CharFilter(method='filter_affiliation',
                                label='Affiliation')
    is_investigator = df.BooleanFilter(method='filter_is_investigator',
                                       widget=CBooleanWidget(empty='----'),
                                       label='Is investigator?')
    last_updated = df.DateTimeFilter(field_name='last_updated', lookup_expr='gte',
                                     label='Last updated')

    o = df.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('last_name', 'last_name'),
            ('first_name', 'first_name'),
            ('last_updated', 'last_updated'),
        ),

        field_labels={
            'last_name': 'Surname',
            'first_name': 'Forename',
            'last_updated': 'Last updated',
        }
    )

    class Meta(object):
        model = Person
        fields = ['name', 'last_name', 'first_name', 'is_investigator',
                  'affiliation']

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        value_parts = value.split()
        q = Q()
        for part in value_parts:
            q &= (Q(first_name__icontains=part) | Q(last_name__icontains=part))

        return queryset.filter(q)

    def filter_is_investigator(self, queryset, name, value):
        queryset = queryset.annotate(num_investigations=Count('investigator'))
        if value:
            return queryset.filter(num_investigations__gt=0)
        return queryset.filter(num_investigations=0)

    def filter_location(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(locations__name__icontains=value)

    def filter_affiliation(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(affiliations__name__icontains=value)


class LocationFilter(filters.FilterSet):
    last_updated = df.DateTimeFilter(field_name='last_updated', lookup_expr='gte',
                                     label='Last updated')
    name = df.CharFilter(lookup_expr='icontains')
                                     
    o = df.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('name', 'name'), ('last_updated', 'last_updated'),
        ),

        field_labels={
            'name': 'Name', 'last_updated': 'Last updated',
        }
    )

    class Meta(object):
        model = Location
        fields = ['name', 'validated']


