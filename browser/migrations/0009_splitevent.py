# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browser', '0008_auto_20160803_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplitEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_instance_id', models.PositiveIntegerField()),
                ('child_instance_id', models.PositiveIntegerField()),
                ('changed_by', models.ForeignKey(related_name='edited_splitevent', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('child_type', models.ForeignKey(related_name='split_from', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('original_type', models.ForeignKey(related_name='split_to', to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
    ]
