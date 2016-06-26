from django.db import models


class URIMixin(models.Model):
    uri = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True


class YearMixin(models.Model):
    year = models.IntegerField()

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Course(URIMixin, NameMixin, YearMixin):
    attendees = models.ManyToManyField('Person', through='Attendance',
                                       related_name='courses')
    is_part_of = models.ManyToManyField('CourseGroup', through='PartOf',
                                        related_name='courses')

    @property
    def primary_coursegroup(self):
        return self.is_part_of.all()[0]

    @property
    def number_of_attendees(self):
        return self.attendees.count()


class CourseGroup(URIMixin, NameMixin):
    @property
    def number_of_courses(self):
        return self.courses.count()


class Institution(URIMixin, NameMixin):
    authority = models.ForeignKey('KnownInstitution', blank=True, null=True,
                                  help_text="""
    Use this field to specify a known institution (i.e. a location with an entry
    in the Conceptpower name authority).""")

    @property
    def number_of_affiliates(self):
        return self.affiliates.count()


class Location(URIMixin, NameMixin):
    authority = models.ForeignKey('KnownLocation', blank=True, null=True,
                                  help_text="""
    Use this field to specify a known location (i.e. a location with an entry
    in the GeoNames database).""")

    @property
    def number_of_denizens(self):
        return self.denizens.distinct('pk').count()


class Person(URIMixin):
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


    @property
    def name(self):
        return ' '.join([self.first_name, self.last_name])

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

    def __unicode__(self):
        return self.name


class Affiliation(YearMixin):
    person = models.ForeignKey('Person')
    institution = models.ForeignKey('Institution')
    position = models.CharField(max_length=255, blank=True)


class Attendance(YearMixin):
    person = models.ForeignKey('Person')
    course = models.ForeignKey('Course')

    role = models.CharField(max_length=255, blank=True)


class PartOf(YearMixin):
    course = models.ForeignKey('Course')
    coursegroup = models.ForeignKey('CourseGroup')


class Localization(YearMixin):
    person = models.ForeignKey('Person')
    location = models.ForeignKey('Location')


class Investigator(YearMixin):
    person = models.ForeignKey('Person')
    subject = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)


class KnownLocation(NameMixin):
    """
    A :class:`.KnownLocation` is a location with an entry in the GeoNames
    database.
    """
    geonames_uri = models.CharField(max_length=255, blank=True, null=True)
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
    latitude = models.FloatField(help_text='Decimal latitude, e.g. 48.1295')
    latitude_direction = models.CharField(max_length=1, choices=LAT_CARDINAL,
                                          help_text="""
    If the location is in the northern hemisphere, and has a positive latitude,
    then the latitude cardinality is North.""")

    longitude = models.FloatField(help_text='Decimal longitude, e.g. 128.7490')
    longitude_direction = models.CharField(max_length=1, choices=LON_CARDINAL,
                                           help_text="""
    If the location is in the western hemisphere, and has a negative longitude,
    then the longitude cardinality is East.""")


class KnownPerson(NameMixin):
    """
    A :class:`.KnownPerson` is a person for which an entry exists in the
    Conceptpower name authority.
    """

    conceptpower_uri = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)


class KnownInstitution(NameMixin):
    """
    A :class:`.KnownInstitution` is an institution for which an entry exists in
    the Conceptpower name authority.
    """

    conceptpower_uri = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
