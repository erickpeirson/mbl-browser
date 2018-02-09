from django.db import models
from simple_history.models import HistoricalRecords
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey

from uuid import uuid4
from django.conf import settings


def generate_uri(model):
    return '/'.join([settings.URI_NAMESPACE, model.__name__.lower(), str(uuid4())])


class URIMixin(models.Model):
    uri = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.uri:
            self.uri = generate_uri(self.__class__)
        super(URIMixin, self).save(*args, **kwargs)


class YearMixin(models.Model):
    year = models.IntegerField()

    class Meta:
        abstract = True


class LastUpdatedMixin(models.Model):
    """
    Model must aleady have an history field.
    """
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(auto_now=True)


class CuratedMixin(models.Model):
    validated = models.BooleanField(default=False, help_text="Indicates that"
                                    " a record has been examined for accuracy."
                                    " This does not necessarily mean that the"
                                    " record has been disambiguated with"
                                    " respect to an authority accord.")
    validated_by = models.ForeignKey('auth.User', null=True, blank=True)
    validated_on = models.DateTimeField(null=True, blank=True)

    split_to = GenericRelation('SplitEvent',
                               content_type_field='original_type',
                               object_id_field='original_instance_id')

    split_from = GenericRelation('SplitEvent',
                                 content_type_field='child_type',
                                 object_id_field='child_instance_id')

    merge_to = GenericRelation('MergeEvent',
                               content_type_field='parent_type',
                               object_id_field='parent_instance_id')

    merge_from = GenericRelation('MergeEvent',
                                 content_type_field='child_type',
                                 object_id_field='child_instance_id')

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Course(URIMixin, NameMixin, YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    attendees = models.ManyToManyField('Person', through='Attendance',
                                       related_name='courses')
    is_part_of = models.ManyToManyField('CourseGroup', through='PartOf',
                                        related_name='courses')

    changed_by = models.ForeignKey('auth.User', related_name='edited_courses')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def primary_coursegroup(self):
        return self.is_part_of.all()[0]

    @property
    def number_of_attendees(self):
        return self.attendees.count()

    def get_absolute_url(self):
        return reverse('course', args=[self.id])

    def can_delete(self):
        return self.attendees.count() == 0


class CourseGroup(URIMixin, NameMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    changed_by = models.ForeignKey('auth.User', related_name='edited_coursegroups')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def number_of_courses(self):
        return self.courses.count()

    def get_absolute_url(self):
        return reverse('coursegroup', args=[self.id])


class Institution(URIMixin, NameMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    authority = models.ForeignKey('KnownInstitution', blank=True, null=True,
                                  help_text="""
    Use this field to specify a known institution (i.e. a location with an entry
    in the Conceptpower name authority).""")

    changed_by = models.ForeignKey('auth.User', related_name='edited_institutions')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def number_of_affiliates(self):
        return self.affiliates.count()

    def get_absolute_url(self):
        return reverse('institution', args=[self.id])


class Location(URIMixin, NameMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    authority = models.ForeignKey('KnownLocation', blank=True, null=True,
                                  help_text="""
    Use this field to specify a known location (i.e. a location with an entry
    in the GeoNames database).""")

    changed_by = models.ForeignKey('auth.User', related_name='edited_locations')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def number_of_denizens(self):
        return self.denizens.distinct('pk').count()

    def get_absolute_url(self):
        return reverse('location', args=[self.id])


class Person(URIMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True)
    affiliations = models.ManyToManyField('Institution', through='Affiliation',
                                          related_name='affiliates')
    locations = models.ManyToManyField('Location', through='Localization',
                                       related_name='denizens')
    authority  = models.ForeignKey('KnownPerson', blank=True, null=True,
                                   help_text="""
    Use this field to specify a known person (i.e. a person with an entry in
    the Conceptpower name authority).""")

    changed_by = models.ForeignKey('auth.User', related_name='edited_persons')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    @property
    def name(self):
        if hasattr(self, 'first_name'):
            return ' '.join([self.first_name, self.last_name])
        return self.last_name

    @property
    def number_of_courses(self):
        return self.courses.distinct('pk').count()

    @property
    def number_of_affiliations(self):
        return self.affiliations.distinct('pk').count()

    @property
    def number_of_locations(self):
        return self.locations.distinct('pk').count()

    @property
    def is_investigator(self):
        return self.investigator_set.count() > 0

    @property
    def has_position(self):
        return self.position_set.count() > 0

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person', args=[self.id])


class Affiliation(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    person = models.ForeignKey('Person')
    institution = models.ForeignKey('Institution')
    position = models.CharField(max_length=255, blank=True)

    changed_by = models.ForeignKey('auth.User', related_name='edited_affiliations')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        if self.position:
            return u'%s in %i as %s' % (self.institution.name, self.year, self.position)
        return u'%s in %i' % (self.institution.name, self.year)


class Attendance(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    person = models.ForeignKey('Person')
    course = models.ForeignKey('Course')

    role = models.CharField(max_length=255, blank=True)

    changed_by = models.ForeignKey('auth.User', related_name='edited_attendances')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return u'%s as %s' % (self.course.name, self.role)


class PartOf(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    course = models.ForeignKey('Course')
    coursegroup = models.ForeignKey('CourseGroup')

    changed_by = models.ForeignKey('auth.User', related_name='edited_part_of')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Localization(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    person = models.ForeignKey('Person')
    location = models.ForeignKey('Location')

    changed_by = models.ForeignKey('auth.User', related_name='edited_localizations')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        return u'%s in %i' % (self.location.name, self.year)

    @property
    def as_person_locale(self):
        return u'%s in %i' % (self.person.__unicode__(), self.year)


class Investigator(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    person = models.ForeignKey('Person')
    subject = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)

    changed_by = models.ForeignKey('auth.User', related_name='edited_investigators')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        rep = u''
        if self.role:
            rep += u'Role: %s' % self.role
        if self.subject:
            if self.role:
                rep += u', '
            rep += u'Subject: %s' % self.subject
        if self.subject or self.role:
            rep += u', in %s' % self.year
        else:
            rep = u'Investigator in %i' % self.year
        return rep


class KnownLocation(NameMixin, CuratedMixin, LastUpdatedMixin):
    """
    """
    history = HistoricalRecords()
    external_uri = models.CharField(max_length=255, blank=True, null=True,
                                    help_text="Enter a resolvable URI from a"
                                    " geographic database, e.g. OpenStreetMap"
                                    " or GeoNames. If using OpenStreetMap,"
                                    " this can be the 'share URL'; be sure to"
                                    " select 'include marker.'")
    geo_uri = models.CharField(max_length=255, blank=True, null=True,
                               help_text="e.g. 'geo:39.96511,-75.19281?z=19'."
                               " For more information about Geo URIs, see"
                               " https://en.wikipedia.org/wiki/Geo_URI_scheme")
    description = models.TextField(null=True, blank=True)

    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    LAT_CARDINAL = (
        (NORTH, 'North'),
        (SOUTH, 'South')
    )
    LON_CARDINAL = (
        (EAST, 'East'),
        (WEST, 'West')
    )
    latitude = models.FloatField(null=True, blank=True, help_text='Decimal latitude, e.g. 48.1295')
    latitude_direction = models.CharField(max_length=1, null=True, blank=True,
                                          choices=LAT_CARDINAL, help_text="""
    If the location is in the northern hemisphere, and has a positive latitude,
    then the latitude cardinality is North.""")

    longitude = models.FloatField(null=True, blank=True,
                                  help_text='Decimal longitude, e.g. 128.7490')
    longitude_direction = models.CharField(max_length=1, null=True, blank=True,
                                           choices=LON_CARDINAL, help_text="""
    If the location is in the western hemisphere, and has a negative longitude,
    then the longitude cardinality is East.""")

    changed_by = models.ForeignKey('auth.User', related_name='edited_known_locations')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class KnownPerson(NameMixin, CuratedMixin, LastUpdatedMixin):
    """
    A :class:`.KnownPerson` is a person for which an entry exists in the
    Conceptpower name authority.
    """
    history = HistoricalRecords()

    conceptpower_uri = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    changed_by = models.ForeignKey('auth.User', related_name='edited_known_persons')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class KnownInstitution(NameMixin, CuratedMixin, LastUpdatedMixin):
    """
    A :class:`.KnownInstitution` is an institution for which an entry exists in
    the Conceptpower name authority.
    """
    history = HistoricalRecords()
    conceptpower_uri = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    changed_by = models.ForeignKey('auth.User', related_name='edited_known_institutions')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class AlterRelationEvent(models.Model):
    affecting_type = models.ForeignKey(ContentType, related_name='altered_by')
    affecting_instance_id = models.PositiveIntegerField()
    affecting = GenericForeignKey('affecting_type', 'affecting_instance_id')

    affected_by_type = models.ForeignKey(ContentType, related_name='altered')
    affected_by_instance_id = models.PositiveIntegerField()
    affected_by = GenericForeignKey('affected_by_type', 'affected_by_instance_id')

    occurred = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('auth.User', related_name='edited_alterrelationevent')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class SplitEvent(models.Model):
    original_type = models.ForeignKey(ContentType, related_name='split_to',
                                      on_delete=models.CASCADE)
    original_instance_id = models.PositiveIntegerField()
    original = GenericForeignKey('original_type', 'original_instance_id')

    child_type = models.ForeignKey(ContentType, related_name='split_from',
                                      on_delete=models.CASCADE)
    child_instance_id = models.PositiveIntegerField()
    child = GenericForeignKey('child_type', 'child_instance_id')

    occurred = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('auth.User', related_name='edited_splitevent')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class MergeEvent(models.Model):
    parent_type = models.ForeignKey(ContentType, related_name='merged_from',
                                      on_delete=models.CASCADE)
    parent_instance_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_instance_id')

    child_type = models.ForeignKey(ContentType, related_name='merged_to',
                                      on_delete=models.CASCADE)
    child_instance_id = models.PositiveIntegerField()
    child = GenericForeignKey('child_type', 'child_instance_id')

    occurred = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('auth.User', related_name='edited_mergeevent')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


class Position(YearMixin, CuratedMixin, LastUpdatedMixin):
    history = HistoricalRecords()
    person = models.ForeignKey('Person')
    subject = models.CharField(max_length=255, blank=True)
    CORPORATION_MEMBER = 'CM'
    TRUSTEE = 'TR'
    FRIDAY_EVENING_LECTURER = 'FEL'
    role_choices = ((CORPORATION_MEMBER, 'Corporation Member'), (TRUSTEE, 'Trustee'),
                    (FRIDAY_EVENING_LECTURER, 'Friday Evening Lecturer'))
    role = models.CharField(max_length=255, blank=False, choices=role_choices)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    changed_by = models.ForeignKey('auth.User', related_name='edited_position')

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __unicode__(self):
        rep = u''
        if self.role:
            rep += u'Role: %s' % self.role
        if self.subject:
            if self.role:
                rep += u' '
            rep += u'Subject: %s' % self.subject
        if self.subject or self.role:
            rep += u' in %s' % self.year
        else:
            rep = u'Investigator in %i' % self.year
        return rep
