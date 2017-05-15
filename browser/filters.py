import django_filters
from django.db.models import Count
from django.utils.translation import ugettext as _
from django.db.models import Q

from rest_framework import filters

from browser.models import *


class ConfigurableBooleanWidget(django_filters.widgets.BooleanWidget):
    """
    Overrides :class:`django_filters.widgets.BooleanWidget` in order to allow
    configuration of the empty option.
    """
    def __init__(self, attrs=None, empty=None):
        choices = (('', _(empty) if empty else _('Unknown')),
                   ('true', _('Yes')),
                   ('false', _('No')))
        super(django_filters.widgets.BooleanWidget, self).__init__(attrs, choices)


class CourseFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    occurred_from = django_filters.NumberFilter(name='year', lookup_type='gte')
    occurred_through = django_filters.NumberFilter(name='year', lookup_type='lte')

    class Meta:
        model = Course
        fields = ['name', 'occurred_from', 'occurred_through',]
        order_by = [
            ('name', 'Name (ascending)'),
            ('-name', 'Name (descending)')
        ]


class InstitutionFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_type='icontains')

    class Meta:
        model = Institution
        fields = ['name', ]

from django.db.models import Max, Min

class CourseGroupFilter(filters.FilterSet):
    name = django_filters.CharFilter(name='name', lookup_type='icontains')
    occurred_from = django_filters.MethodFilter()
    occurred_through = django_filters.MethodFilter()

    class Meta:
        model = CourseGroup
        fields = ['name', ]

        order_by = [
            ('name', 'Name (ascending)'),
            ('-name', 'Name (descending)')
        ]

    def filter_occurred_from(self, queryset, value):
        if not value:
            return queryset
        return queryset.annotate(latest_course=Max('courses__year')).filter(latest_course__gte=value)

    def filter_occurred_through(self, queryset, value):
        if not value:
            return queryset
        return queryset.annotate(earliest_course=Min('courses__year')).filter(earliest_course__lte=value)


class PersonFilter(filters.FilterSet):
    last_name = django_filters.CharFilter(name='last_name', lookup_type='icontains')
    first_name = django_filters.CharFilter(name='first_name', lookup_type='icontains')
    location = django_filters.MethodFilter()
    affiliation = django_filters.MethodFilter()
    is_investigator = django_filters.MethodFilter(widget=ConfigurableBooleanWidget(empty='----'))
    name = django_filters.MethodFilter()

    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'is_investigator', 'affiliation']

    def filter_name(self, queryset, value):
        if not value:
            return queryset
        value_parts = value.split()
        q = Q()
        for part in value_parts:
            q &= (Q(first_name__icontains=part) | Q(last_name__icontains=part))

        return queryset.filter(q)

    def filter_is_investigator(self, queryset, value):
        queryset = queryset.annotate(num_investigations=Count('investigator'))
        if value:
            return queryset.filter(num_investigations__gt=0)
        return queryset.filter(num_investigations=0)

    def filter_location(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(locations__name__icontains=value)

    def filter_affiliation(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(affiliations__name__icontains=value)


class LocationFilter(filters.FilterSet):

    class Meta:
        model = Location
        fields = ['name', 'validated']

        order_by = [
            ('name', 'Name (ascending)'),
            ('-name', 'Name (descending)')
        ]
