# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0010_auto_20160804_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalknownlocation',
            old_name='geonames_uri',
            new_name='external_uri',
        ),
        migrations.RenameField(
            model_name='knownlocation',
            old_name='geonames_uri',
            new_name='external_uri',
        ),
        migrations.AddField(
            model_name='historicalknownlocation',
            name='geo_uri',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='geo_uri',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
