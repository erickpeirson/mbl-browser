# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browser', '0015_alterrelationevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='alterrelationevent',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_alterrelationevent', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alterrelationevent',
            name='occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 10, 17, 23, 36, 773716, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mergeevent',
            name='occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 10, 17, 23, 42, 439154, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='splitevent',
            name='occurred',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 10, 17, 23, 47, 709934, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
