# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0009_splitevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalaffiliation',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalcoursegroup',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalinstitution',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalinvestigator',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalknowninstitution',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalknownlocation',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalknownperson',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicallocalization',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicallocation',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalpartof',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='investigator',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knowninstitution',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knownperson',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='localization',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='partof',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='validated_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='course',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalaffiliation',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalattendance',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalcoursegroup',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalinstitution',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalinvestigator',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalknowninstitution',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalknownperson',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicallocalization',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicallocation',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalpartof',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='historicalperson',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='investigator',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='knowninstitution',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='knownperson',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='localization',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='location',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='partof',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
        migrations.AlterField(
            model_name='person',
            name='validated',
            field=models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.'),
        ),
    ]
