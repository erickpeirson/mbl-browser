from django import forms

from browser.models import *

import datetime


class CourseGroupForm(forms.ModelForm):
    class Meta:
        model = CourseGroup
        fields = ['name', 'validated']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'validated']


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'validated']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'validated']


class KnownLocationForm(forms.ModelForm):
    class Meta:
        model = KnownLocation
        fields = ['external_uri', 'geo_uri']


class PersonForm(forms.ModelForm):
    conceptpower_uri = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'validated']


class DenizenMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.as_person_locale


class MergeLocationForm(forms.Form):
    merge_into = forms.ModelChoiceField(queryset=Location.objects.order_by('name'), required=True)

    def __init__(self, *args, **kwargs):
        self.locations = kwargs.pop('locations', None)
        super(MergeLocationForm, self).__init__(*args, **kwargs)
        self.fields['merge_into'].queryset = self.fields['merge_into'].queryset.filter(pk__in=self.locations)

    def save(self, user):
        if self.locations is None:
            raise RuntimeError('no selected people')

        parent = self.cleaned_data.get('merge_into')
        for location in self.fields['merge_into'].queryset:
            if location == parent:
                continue

            merge = MergeEvent.objects.create(**{
                'parent': parent,
                'child': location,
                'changed_by': user,
            })

            for field in ['denizens']:
                for relation in getattr(location, field).all():
                    relation.location = parent
                    relation.save()

                    AlterRelationEvent.objects.create(**{
                        'affected_by': merge,
                        'affecting': relation,
                        'changed_by': user,
                    })

        return parent


class SplitLocationForm(forms.Form):
    name = forms.CharField(max_length=255)
    validated = forms.BooleanField(required=False,  help_text="Indicates that"
                                    " a record has been examined for accuracy."
                                    " This does not necessarily mean that the"
                                    " record has been disambiguated with"
                                    " respect to an authority accord.")

    denizens = DenizenMultipleChoiceField(queryset=Localization.objects.order_by('person__last_name', 'year'),
                                              required=False,
                                              help_text="Any people that you"
                                              " select from this list will be"
                                              " removed from the original"
                                              " record and associated with the"
                                              " new record.")

    def __init__(self, *args, **kwargs):
        self.location = kwargs.pop('location', None)
        super(SplitLocationForm, self).__init__(*args, **kwargs)
        if self.location is not None:
            self.fields['denizens'].queryset = self.fields['denizens'].queryset.filter(location=self.location)

    def save(self, user):
        if self.location is None:
            raise RuntimeError('person is not set')

        location_data = {
            'name': self.cleaned_data['name'],
            'changed_by': user,
            'uri': generate_uri(Location),
        }
        validated = self.cleaned_data.get('validated', False)
        if validated and not self.location.validated:
            location_data.update({
                'validated': validated,
                'validated_by': user,
                'validated_on': datetime.datetime.now(),
            })
        new_location = Location.objects.create(**location_data)

        split = SplitEvent.objects.create(**{
            'original': self.location,
            'child': new_location,
            'changed_by': user,
        })

        for relation in ['denizens']:
            for instance in self.cleaned_data[relation]:
                instance.location = new_location
                instance.save()

                AlterRelationEvent.objects.create(**{
                    'affected_by': split,
                    'affecting': instance,
                    'changed_by': user,
                })

        return new_location


class MergePersonForm(forms.Form):
    merge_into = forms.ModelChoiceField(queryset=Person.objects.order_by('last_name', 'first_name'), required=True)

    def __init__(self, *args, **kwargs):
        self.people = kwargs.pop('people', None)
        super(MergePersonForm, self).__init__(*args, **kwargs)
        self.fields['merge_into'].queryset = self.fields['merge_into'].queryset.filter(pk__in=self.people)

    def save(self, user):
        if self.people is None:
            raise RuntimeError('no selected people')

        parent = self.cleaned_data.get('merge_into')
        for person in self.fields['merge_into'].queryset:
            if person == parent:
                continue

            merge = MergeEvent.objects.create(**{
                'parent': parent,
                'child': person,
                'changed_by': user,
            })

            for field in ['affiliations', 'attendance_set', 'localization_set', 'investigator_set']:
                for relation in getattr(person, field).all():
                    relation.person = parent
                    relation.save()

                    AlterRelationEvent.objects.create(**{
                        'affected_by': merge,
                        'affecting': relation,
                        'changed_by': user,
                    })

        return parent


class SplitPersonForm(forms.Form):
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)
    affiliations = forms.ModelMultipleChoiceField(queryset=Affiliation.objects.order_by('institution__name', 'year'), required=False)
    attendances = forms.ModelMultipleChoiceField(queryset=Attendance.objects.order_by('course__name', 'year'), required=False)
    localizations = forms.ModelMultipleChoiceField(queryset=Localization.objects.order_by('location__name', 'year'), required=False)
    investigations = forms.ModelMultipleChoiceField(queryset=Investigator.objects.order_by('role', 'year'), required=False)

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person', None)
        super(SplitPersonForm, self).__init__(*args, **kwargs)
        if self.person is not None:
            self.fields['affiliations'].queryset = self.fields['affiliations'].queryset.filter(person=self.person)
            self.fields['attendances'].queryset = self.fields['attendances'].queryset.filter(person=self.person)
            self.fields['localizations'].queryset = self.fields['localizations'].queryset.filter(person=self.person)
            self.fields['investigations'].queryset = self.fields['investigations'].queryset.filter(person=self.person)

    def save(self, user):
        if self.person is None:
            raise RuntimeError('person is not set')

        new_person = Person.objects.create(**{
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'changed_by': user,
            'uri': generate_uri(Person),
        })

        split = SplitEvent.objects.create(**{
            'original': self.person,
            'child': new_person,
            'changed_by': user,
        })

        for relation in ['affiliations', 'attendances', 'localizations', 'investigations']:
            for instance in self.cleaned_data[relation]:
                instance.person = new_person
                instance.save()
                AlterRelationEvent.objects.create(**{
                    'affected_by': split,
                    'affecting': instance,
                    'changed_by': user,
                })
        return new_person
