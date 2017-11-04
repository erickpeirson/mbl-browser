# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-03 21:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browser', '0017_auto_20170511_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPosition',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('last_updated', models.DateTimeField(blank=True, editable=False)),
                ('validated', models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.')),
                ('validated_on', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('role', models.CharField(blank=True, choices=[(b'Corporation Member', b'Corporation Member'), (b'Trustee', b'Trustee'), (b'Friday Evening Lecturer', b'Friday Evening Lecturer')], max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='browser.Person')),
                ('validated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical position',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField(default=False, help_text=b'Indicates that a record has been examined for accuracy. This does not necessarily mean that the record has been disambiguated with respect to an authority accord.')),
                ('validated_on', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('role', models.CharField(blank=True, choices=[(b'Corporation Member', b'Corporation Member'), (b'Trustee', b'Trustee'), (b'Friday Evening Lecturer', b'Friday Evening Lecturer')], max_length=255)),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edited_position', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='browser.Person')),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
