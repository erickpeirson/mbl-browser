# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0002_auto_20151012_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('conceptpower_uri', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='latitude',
            field=models.FloatField(help_text=b'Decimal latitude, e.g. 48.1295'),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='latitude_direction',
            field=models.CharField(help_text=b'\n    If the location is in the northern hemisphere, and has a positive latitude,\n    then the latitude cardinality is North.', max_length=1, choices=[(b'N', b'North'), (b'S', b'South')]),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='longitude',
            field=models.FloatField(help_text=b'Decimal longitude, e.g. 128.7490'),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='longitude_direction',
            field=models.CharField(help_text=b'\n    If the location is in the western hemisphere, and has a negative longitude,\n    then the longitude cardinality is East.', max_length=1, choices=[(b'E', b'East'), (b'W', b'West')]),
        ),
        migrations.AlterField(
            model_name='location',
            name='authority',
            field=models.ForeignKey(blank=True, to='browser.KnownLocation', help_text=b'\n    Use this field to specify a known location (i.e. a location with an entry\n    in the GeoNames database).', null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='authority',
            field=models.ForeignKey(blank=True, to='browser.KnownPerson', help_text=b'\n    Use this field to specify a known person (i.e. a person with an entry in\n    the Conceptpower name authority).', null=True),
        ),
    ]
