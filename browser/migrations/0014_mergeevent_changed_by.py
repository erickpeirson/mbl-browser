# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browser', '0013_auto_20160810_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='mergeevent',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_mergeevent', default=1, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
