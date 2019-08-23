# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('browser', '0014_mergeevent_changed_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlterRelationEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('affecting_instance_id', models.PositiveIntegerField()),
                ('affected_by_instance_id', models.PositiveIntegerField()),
                ('affected_by_type', models.ForeignKey(related_name='altered', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('affecting_type', models.ForeignKey(related_name='altered_by', to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
        ),
    ]
