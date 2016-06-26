from rest_framework import viewsets

from browser.models import *
from browser.serializers import *
from browser.filters import *


class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CourseGroupFilter

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return CourseGroupListSerializer
        return CourseGroupDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PersonFilter

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return PersonListSerializer
        return PersonDetailSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return InstitutionListSerializer
        return InstitutionDetailSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return LocationListSerializer
        return LocationDetailSerializer
