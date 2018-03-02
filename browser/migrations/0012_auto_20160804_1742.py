# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0011_auto_20160804_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='latitude',
            field=models.FloatField(help_text=b'Decimal latitude, e.g. 48.1295', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='latitude_direction',
            field=models.CharField(blank=True, max_length=1, null=True, help_text=b'\n    If the location is in the northern hemisphere, and has a positive latitude,\n    then the latitude cardinality is North.', choices=[(b'N', b'North'), (b'S', b'South')]),
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='longitude',
            field=models.FloatField(help_text=b'Decimal longitude, e.g. 128.7490', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='longitude_direction',
            field=models.CharField(blank=True, max_length=1, null=True, help_text=b'\n    If the location is in the western hemisphere, and has a negative longitude,\n    then the longitude cardinality is East.', choices=[(b'E', b'East'), (b'W', b'West')]),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='latitude',
            field=models.FloatField(help_text=b'Decimal latitude, e.g. 48.1295', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='latitude_direction',
            field=models.CharField(blank=True, max_length=1, null=True, help_text=b'\n    If the location is in the northern hemisphere, and has a positive latitude,\n    then the latitude cardinality is North.', choices=[(b'N', b'North'), (b'S', b'South')]),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='longitude',
            field=models.FloatField(help_text=b'Decimal longitude, e.g. 128.7490', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='longitude_direction',
            field=models.CharField(blank=True, max_length=1, null=True, help_text=b'\n    If the location is in the western hemisphere, and has a negative longitude,\n    then the longitude cardinality is East.', choices=[(b'E', b'East'), (b'W', b'West')]),
        ),
    ]
