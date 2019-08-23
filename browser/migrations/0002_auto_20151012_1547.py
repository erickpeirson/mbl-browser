# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('geonames_uri', models.CharField(max_length=255, null=True, blank=True)),
                ('latitude', models.FloatField()),
                ('latitude_direction', models.CharField(max_length=1, choices=[(b'N', b'North'), (b'S', b'South')])),
                ('longitude', models.FloatField()),
                ('longitude_direction', models.CharField(max_length=1, choices=[(b'E', b'East'), (b'W', b'West')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='location',
            name='authority',
            field=models.ForeignKey(blank=True, to='browser.KnownLocation', null=True, on_delete=models.CASCADE),
        ),
    ]
