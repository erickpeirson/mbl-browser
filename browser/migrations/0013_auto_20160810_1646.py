# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('browser', '0012_auto_20160804_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_instance_id', models.PositiveIntegerField()),
                ('child_instance_id', models.PositiveIntegerField()),
                ('child_type', models.ForeignKey(related_name='merged_to', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('parent_type', models.ForeignKey(related_name='merged_from', to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='external_uri',
            field=models.CharField(help_text=b"Enter a resolvable URI from a geographic database, e.g. OpenStreetMap or GeoNames. If using OpenStreetMap, this can be the 'share URL'; be sure to select 'include marker.'", max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalknownlocation',
            name='geo_uri',
            field=models.CharField(help_text=b"e.g. 'geo:39.96511,-75.19281?z=19'. For more information about Geo URIs, see https://en.wikipedia.org/wiki/Geo_URI_scheme", max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='external_uri',
            field=models.CharField(help_text=b"Enter a resolvable URI from a geographic database, e.g. OpenStreetMap or GeoNames. If using OpenStreetMap, this can be the 'share URL'; be sure to select 'include marker.'", max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='geo_uri',
            field=models.CharField(help_text=b"e.g. 'geo:39.96511,-75.19281?z=19'. For more information about Geo URIs, see https://en.wikipedia.org/wiki/Geo_URI_scheme", max_length=255, null=True, blank=True),
        ),
    ]
