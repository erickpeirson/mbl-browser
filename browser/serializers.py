from rest_framework import serializers

from browser.models import *
from django.contrib.auth.models import User

from collections import defaultdict


class MockObject(dict):
    """
    The :class:`serializers.HyperlinkedIdentityField` in relies on
    ``__getattr__``, but we want to use ``values`` (to save on db overhead)
    which returns a dict.
    """

    def __getattr__(self, key):
        """
        Translates a ``__getattr__()`` into a ``get()``.
        """
        return self.get(key)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class KnownPersonSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer()

    class Meta:
        model = KnownPerson
        fields = ('conceptpower_uri', 'description', 'changed_by',
                  'last_updated')


class KnownLocationSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer()

    class Meta:
        model = KnownLocation
        fields = ('external_uri', 'geo_uri', 'description', 'changed_by',
                  'last_updated')


class KnownInstitutionSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer()

    class Meta:
        model = KnownInstitution
        fields = ('conceptpower_uri', 'description', 'changed_by',
                  'last_updated')


class DenizenSerializer(serializers.Serializer):
    """
    From the perspective of a :class:`.Location`\.
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    year = serializers.ListField()
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class LocationListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'url', 'number_of_denizens', 'last_updated',
                  'validated', 'validated_by', 'validated_on')


class LocationDetailSerializer(serializers.HyperlinkedModelSerializer):
    denizens = serializers.SerializerMethodField('has_denizens')
    authority = KnownLocationSerializer()

    class Meta:
        model = Location
        fields = ('name', 'url', 'denizens', 'number_of_denizens',
                  'last_updated', 'validated', 'validated_by', 'validated_on',
                  'authority')

    def has_denizens(self, obj):
        """
        Group :class:`.Localization` instances by :class:`.Person`\.

        Display only one entry per person per year.
        """

        afields = ['person_id', 'year']
        aqs = Localization.objects.filter(location_id=obj.id).distinct(*afields)

        person_locations = defaultdict(list)
        for localization in aqs.values('last_updated', *afields):
            person_locations[localization['person_id']].append(localization['year'])

        pfields = ['last_name', 'first_name', 'pk', 'last_updated', 'validated',
                   'validated_by__username', 'validated_on']
        qs = []
        for person in obj.denizens.distinct('pk').values(*pfields):
            person['year'] = person_locations[person['pk']]
            person['validated_by'] = person['validated_by__username']
            qs.append(MockObject(person))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = DenizenSerializer(qs, many=True, context=context)
        return serializer.data


class PositionSerializer(serializers.Serializer):
    position = serializers.CharField(max_length=255)
    year = serializers.IntegerField(default=0)
    last_updated = serializers.DateTimeField()


class AffiliateSerializer(serializers.Serializer):
    """
    From the perspective of an :class:`.Institution`\.
    """
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    positions = PositionSerializer(many=True)
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class AffiliationSerializer(serializers.Serializer):
    """
    From the perspective of a :class:`.Person`\.
    """
    name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='institution-detail')
    positions = PositionSerializer(many=True)
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class InstitutionDetailSerializer(serializers.HyperlinkedModelSerializer):
    affiliates = serializers.SerializerMethodField('affiliated_people')
    authority = KnownInstitutionSerializer()

    class Meta:
        model = Institution
        fields = ('name', 'url', 'affiliates', 'number_of_affiliates',
                  'last_updated', 'id', 'validated', 'validated_by',
                  'validated_on', 'authority')

    def affiliated_people(self, obj):
        """
        Group :class:`.Affiliation` instances by :class:`.Person`\.

        Display only one entry per person per year, unless there is more than
        one position in that year.
        """

        afields = ['person_id', 'year', 'position']
        aqs = Affiliation.objects.filter(institution_id=obj.id)\
                                 .distinct(*afields)

        person_affiliations = defaultdict(list)
        for affiliation in aqs.values('last_updated', *afields):
            person_affiliations[affiliation['person_id']].append(affiliation)

        pfields = ['last_updated', 'last_name', 'first_name', 'pk',
                   'validated', 'validated_by__username', 'validated_on']
        qs = []
        for person in obj.affiliates.distinct('pk').values(*pfields):
            person['positions'] = person_affiliations[person['pk']]
            person['validated_by'] = person['validated_by__username']
            qs.append(MockObject(person))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = AffiliateSerializer(qs, many=True, context=context)
        return serializer.data


class InstitutionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('name', 'url', 'number_of_affiliates', 'last_updated', 'id',
                  'validated', 'validated_by', 'validated_on')


class LocalizationSerializer(serializers.Serializer):
    """
    From the perspective of a :class:`.Person`\.
    """
    name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='location-detail')
    year = serializers.ListField()
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class InvestigatorSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    role = serializers.CharField(max_length=255)
    year = serializers.IntegerField(default=0)
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class PersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    affiliations = serializers.SerializerMethodField('affiliated_with')
    courses = serializers.SerializerMethodField('attended_courses')
    locations = serializers.SerializerMethodField('has_location')
    investigation = serializers.SerializerMethodField('is_investigator')
    authority = KnownPersonSerializer(read_only=True)

    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'url', 'number_of_courses',
                  'is_investigator', 'number_of_affiliations', 'affiliations',
                  'courses', 'locations', 'investigation', 'uri', 'authority',
                  'last_updated', 'id', 'validated', 'validated_by',
                  'validated_on')


    def affiliated_with(self, obj):
        """
        Group :class:`.Affiliation` instances by :class:`.Institution`\.

        Display only one entry per institution per year, unless there is more
        than one position in that year.
        """

        afields = ['institution_id', 'year', 'position']
        aqs = Affiliation.objects.filter(person_id=obj.id).distinct(*afields)

        institution_affiliations = defaultdict(list)
        for affiliation in aqs.values('last_updated', *afields):
            institution_affiliations[affiliation['institution_id']].append(affiliation)

        pfields = ['name', 'pk', 'last_updated', 'validated',
                   'validated_by__username', 'validated_on']
        qs = []
        for institution in obj.affiliations.distinct('pk').values(*pfields):
            institution['positions'] = institution_affiliations[institution['pk']]
            institution['validated_by'] = institution['validated_by__username']
            qs.append(MockObject(institution))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = AffiliationSerializer(qs, many=True, context=context)
        return serializer.data


    def attended_courses(self, obj):
        """
        Group :class:`.Attendance` instances by :class:`.Course`\.

        Display only one entry per person per year, unless there is more than
        one position in that year.
        """

        afields = ['course_id', 'role']
        aqs = Attendance.objects.filter(person_id=obj.id).distinct(*afields)

        person_attendances = defaultdict(list)
        for attendance in aqs.values('last_updated', *afields):
            person_attendances[attendance['course_id']].append(attendance['role'])

        pfields = ['last_updated', 'name', 'pk', 'validated',
                   'validated_by__username', 'validated_on']
        qs = []
        for course in obj.courses.distinct('pk').values(*pfields):
            course['validated_by'] = course['validated_by__username']
            course['role'] = person_attendances[course['pk']]
            qs.append(MockObject(course))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = AttendanceSerializer(qs, many=True, context=context)
        return serializer.data

    def has_location(self, obj):
        """
        Group :class:`.Localization` instances by :class:`.Course`\.

        Display only one entry per location per year.
        """

        afields = ['location_id', 'year']
        aqs = Localization.objects.filter(person_id=obj.id).distinct(*afields)

        person_locations = defaultdict(list)
        for localization in aqs.values('last_updated', *afields):
            person_locations[localization['location_id']].append(localization['year'])

        pfields = ['name', 'pk', 'last_updated', 'validated',
                   'validated_by__username', 'validated_on']
        qs = []
        for location in obj.locations.distinct('pk').values(*pfields):
            location['year'] = person_locations[location['pk']]
            location['validated_by'] = location['validated_by__username']
            qs.append(MockObject(location))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = LocalizationSerializer(qs, many=True, context=context)
        return serializer.data

    def is_investigator(self, obj):
        qs = obj.investigator_set.all()
        serializer = InvestigatorSerializer(qs, many=True)
        return serializer.data


class PersonListSerializer(serializers.HyperlinkedModelSerializer):
    authority = KnownPersonSerializer(read_only=True)

    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'url', 'number_of_courses',
                  'is_investigator', 'number_of_affiliations', 'uri',
                  'authority', 'last_updated', 'id', 'validated',
                  'validated_by', 'validated_on')


class RoleSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=255)
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class AttendeeSerializer(serializers.Serializer):
    """
    From the perspective of a :class:`.Course`\.
    """
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    role = serializers.ListField()
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class AttendanceSerializer(serializers.Serializer):
    """
    From the perspective of a :class:`.Person`\.
    """
    name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='course-detail')
    role = serializers.ListField()
    last_updated = serializers.DateTimeField()
    validated = serializers.BooleanField()
    validated_by = serializers.CharField()
    validated_on = serializers.DateTimeField()


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):
    is_part_of = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('name', 'url', 'is_part_of', 'attendees',
                  'number_of_attendees', 'year', 'last_updated',
                  'validated', 'validated_by', 'validated_on')

    def get_is_part_of(self, obj):
        qs = obj.is_part_of.distinct('id')
        context = {'request': self._context['request']}
        serializer = CourseGroupListSerializer(qs, many=True, context=context)
        return serializer.data

    def get_attendees(self, obj):
        """
        Group :class:`.Attendance` instances by :class:`.Person`\.

        Display only one entry per person per year, unless there is more than
        one position in that year.
        """

        afields = ['person_id', 'role']
        aqs = Attendance.objects.filter(course_id=obj.id).distinct(*afields)

        person_attendances = defaultdict(list)
        for attendance in aqs.values('last_updated', *afields):
            person_attendances[attendance['person_id']].append(attendance['role'])

        pfields = ['last_name', 'first_name', 'pk', 'last_updated', 'validated',
                   'validated_by__username', 'validated_on']
        qs = []
        for person in obj.attendees.distinct('pk').values(*pfields):
            person['role'] = person_attendances[person['pk']]
            person['validated_by'] = person['validated_by__username']
            qs.append(MockObject(person))

        # HyperlinkedIdentityField requires the HttpRequest to generate an
        #  absolute URL.
        context = {'request': self._context['request']}
        serializer = AttendeeSerializer(qs, many=True, context=context)
        return serializer.data


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'url', 'number_of_attendees', 'year', 'last_updated',
                  'validated', 'validated_by', 'validated_on')


class CourseGroupListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('id', 'name', 'url', 'number_of_courses', 'last_updated',
                  'validated', 'validated_by', 'validated_on')


class CourseGroupDetailSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = CourseGroup
        fields = ('id', 'name', 'url', 'number_of_courses', 'courses',
                  'last_updated', 'validated', 'validated_by', 'validated_on')

    def get_courses(self, obj):
        qs = obj.courses.distinct('id')
        context = {'request': self._context['request']}
        serializer = CourseListSerializer(qs, many=True, context=context)
        return serializer.data
