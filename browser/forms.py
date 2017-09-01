from django import forms

from browser.models import *

import datetime


class CourseGroupForm(forms.ModelForm):
    class Meta:
        model = CourseGroup
        fields = ['name', 'validated']


class GroupForCourseForm(forms.Form):
    group_name = forms.CharField()
    group = forms.ModelChoiceField(queryset=CourseGroup.objects.all(),
                                   required=False,
                                   widget=forms.HiddenInput())
    group_create = forms.BooleanField(required=False, label='Create',
                                      help_text="Create a new group or series"
                                                " for this course.")

    def __init__(self, *args, **kwargs):
        print args, kwargs
        if args:
            initial = kwargs.get('initial', {})
            group_id = args[0].get('group')
            if group_id:
                group = CourseGroup.objects.get(pk=int(group_id))
                initial.update({'group_name': group.name})

        super(GroupForCourseForm, self).__init__(*args, **kwargs)


class CourseInstanceForm(forms.Form):
    name = forms.CharField(help_text='For example: "Botany 1891"')
    year = forms.IntegerField()
    validated = forms.BooleanField(help_text="Indicates that a record has been"
                                   " examined for accuracy. This does not"
                                   " necessarily mean that the record has been"
                                   " disambiguated with respect to an authority"
                                   " accord.", required=False)



class AttendeeForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    required=False,
                                    widget=forms.HiddenInput())
    person_search = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    create_person = forms.BooleanField(required=False, label='Create',
                                       help_text="Create a new person record.")
    create_person_firstname = forms.CharField(required=False, label='Forename',
                                              help_text='May include middle names and/or initials. E.g. "Eric H."')
    create_person_lastname = forms.CharField(required=False, label='Surname',
                                             help_text='May include affixes, e.g. "Jackson Jr."')
    create_person_location = forms.CharField(required=False, label='Location',
                                             help_text="Enter any information that you have about this person's geographic location,"
                                                       " aside from their institutional affiliation, such as an address.")
    role = forms.CharField(help_text='E.g. Faculty, Student, Assistant, Instructor, Director.')

    institution = forms.ModelChoiceField(queryset=Institution.objects.all(),
                                         required=False,
                                         widget=forms.HiddenInput())
    institution_search = forms.CharField(required=False, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    position = forms.CharField(help_text='E.g. Assistant Professor, Graduate Student', required=False)
    create_institution = forms.BooleanField(required=False, label='Create',
                                            help_text="Create a new institution record using the name entered above.")

    def __init__(self, *args, **kwargs):
        if args:
            initial = kwargs.get('initial', {})
            person_id = args[0].get('person')
            if person_id:
                person = Person.objects.get(pk=int(person_id))
                initial.update({'person_search': person.first_name + ' ' + person.last_name})

            institution_id = args[0].get('institution')
            if institution_id:
                institution = Institution.objects.get(pk=int(institution_id))
                initial.update({'institution_search': institution.name})
            kwargs.update({'initial': initial})
        super(AttendeeForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(AttendeeForm, self).clean()
        create_person = cleaned_data.get('create_person')
        person = cleaned_data.get('person')
        create_person_firstname = cleaned_data.get('create_person_firstname')
        create_person_lastname = cleaned_data.get('create_person_lastname')
        create_institution = cleaned_data.get('create_institution')
        institution_search = cleaned_data.get('institution_search')

        if create_person and not create_person_firstname:
            self.add_error('create_person_firstname', 'Please enter a forename')
        if create_person and not create_person_lastname:
            self.add_error('create_person_lastname', 'Please enter a surname')
        if not person and not create_person:
            self.add_error('person_search', 'Please select a person')
        if create_institution and not institution_search:
            self.add_error('institution_search', 'Please enter the name of the institution')
        return cleaned_data


class CourseForm(forms.ModelForm):
    name = forms.CharField(help_text='For example: "Botany 1891"')
    # is_part_of = forms.ModelChoiceField(widget=forms.HiddenInput(),
    #                                     label='Course group/series',
    #                                     queryset=CourseGroup.objects.all())

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


class KnownPersonForm(forms.ModelForm):
    class Meta:
        model = KnownPerson
        fields = ['conceptpower_uri', 'description']


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


class InvestigatorForm(forms.ModelForm):
    class Meta:
        model = Investigator
        fields = ['subject', 'role', 'year']
