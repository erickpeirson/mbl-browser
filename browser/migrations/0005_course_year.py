# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def get_course_year(apps, schema_editor):
    """
    Populate the Course.year field.
    """

    Course = apps.get_model('browser', 'Course')
    for course in Course.objects.all():
        course.year = course.partof_set.all()[0].year
        course.save()


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0004_auto_20151012_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(default=1900),
            preserve_default=False,
        ),
        migrations.RunPython(get_course_year),
    ]
