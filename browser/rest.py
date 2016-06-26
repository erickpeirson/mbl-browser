from rest_framework import serializers, viewsets

from browser.models import *

from collections import defaultdict


class PersonAffiliationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Affiliation
        fields = ('year', 'position', 'institution')


class InstitutionAffiliationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Affiliation
        fields = ('year', 'position', 'person')


class PositionSerializer(serializers.Serializer):
    position = serializers.CharField(max_length=255)
    year = serializers.IntegerField(default=0)


class AffiliateSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')
    positions = PositionSerializer(many=True)


class InstitutionDetailSerializer(serializers.HyperlinkedModelSerializer):
    # affiliates = InstitutionAffiliationSerializer(source='affiliation_set', many=True)
    affiliates = serializers.SerializerMethodField('affiliated_people')

    class Meta:
        model = Institution
        fields = ('name', 'url', 'affiliates')

    def affiliated_people(self, obj):
        class MockPerson(dict):
            """
            The :class:`serializers.HyperlinkedIdentityField` in
            :class:`.AffiliateSerializer` relies on ``__getattr__``, but
            we want to use ``values`` below (to save on db overhead).
            """

            def __getattr__(self, key):
                """
                Translates a ``__getattr__()`` into a ``get()``.
                """
                return self.get(key)

        afields = ['person_id', 'year', 'position']
        aqs = Affiliation.objects.filter(institution_id=obj.id)\
                                 .distinct(*afields)

        person_affiliations = defaultdict(list)
        for affiliation in aqs.values(*afields):
            person_affiliations[affiliation['person_id']].append(affiliation)

        pfields = ['last_name', 'first_name', 'pk']
        qs = []
        for person in obj.affiliates.distinct('pk').values(*pfields):
            person['positions'] = person_affiliations[person['pk']]
            qs.append(MockPerson(person))

        serializer = AffiliateSerializer(qs, many=True, context={'request': self._context['request']})
        return serializer.data



class InstitutionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ('name', 'url')


class PersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    affiliations = PersonAffiliationSerializer(source='affiliation_set', many=True)

    class Meta:
        model = Person
        exclude = ('uri',)


class PersonListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'url')


class CourseGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('name', 'url')


class CourseDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'url', 'is_part_of', 'attendees')


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'url', 'is_part_of')



class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()

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
