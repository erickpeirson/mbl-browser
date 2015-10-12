# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0003_auto_20151012_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnownInstitution',
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
            model_name='institution',
            name='authority',
            field=models.ForeignKey(blank=True, to='browser.KnownInstitution', help_text=b'\n    Use this field to specify a known institution (i.e. a location with an entry\n    in the Conceptpower name authority).', null=True),
        ),
    ]
