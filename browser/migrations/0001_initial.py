# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('position', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('role', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Investigator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('subject', models.CharField(max_length=255, blank=True)),
                ('role', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Localization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PartOf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('course', models.ForeignKey(to='browser.Course')),
                ('coursegroup', models.ForeignKey(to='browser.CourseGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(unique=True, max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255, blank=True)),
                ('affiliations', models.ManyToManyField(related_name='affiliates', through='browser.Affiliation', to='browser.Institution')),
                ('locations', models.ManyToManyField(related_name='denizens', through='browser.Localization', to='browser.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='localization',
            name='location',
            field=models.ForeignKey(to='browser.Location'),
        ),
        migrations.AddField(
            model_name='localization',
            name='person',
            field=models.ForeignKey(to='browser.Person'),
        ),
        migrations.AddField(
            model_name='investigator',
            name='person',
            field=models.ForeignKey(to='browser.Person'),
        ),
        migrations.AddField(
            model_name='course',
            name='attendees',
            field=models.ManyToManyField(related_name='courses', through='browser.Attendance', to='browser.Person'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_part_of',
            field=models.ManyToManyField(related_name='courses', through='browser.PartOf', to='browser.CourseGroup'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(to='browser.Course'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='person',
            field=models.ForeignKey(to='browser.Person'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='institution',
            field=models.ForeignKey(to='browser.Institution'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='person',
            field=models.ForeignKey(to='browser.Person'),
        ),
    ]
