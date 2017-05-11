# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0016_auto_20160810_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 31, 540746, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 39, 421979, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 41, 245537, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 42, 253254, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalaffiliation',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 43, 380419, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 44, 395183, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 45, 433891, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalcoursegroup',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 46, 386112, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalinstitution',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 47, 364658, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalinvestigator',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 48, 273111, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalknowninstitution',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 49, 185374, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalknownlocation',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 50, 149055, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalknownperson',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 51, 227693, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicallocalization',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 52, 225209, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicallocation',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 53, 200975, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalpartof',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 54, 156235, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 55, 82693, tzinfo=utc), editable=False, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institution',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 55, 977340, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investigator',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 57, 267122, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='knowninstitution',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 58, 342348, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 18, 59, 59, 518083, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='knownperson',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 19, 0, 0, 642986, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localization',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 19, 0, 1, 657915, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 19, 0, 2, 602249, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partof',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 19, 0, 3, 589648, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 11, 19, 0, 4, 565206, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
