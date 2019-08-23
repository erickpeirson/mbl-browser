# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browser', '0007_auto_20160803_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='attendance',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='attendance',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='course',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='historicalaffiliation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalaffiliation',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalcoursegroup',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcoursegroup',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalinstitution',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalinstitution',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalinvestigator',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalinvestigator',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalknowninstitution',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalknowninstitution',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalknownlocation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalknownlocation',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalknownperson',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalknownperson',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicallocalization',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicallocalization',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicallocation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicallocation',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalpartof',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpartof',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='validated_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='institution',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='investigator',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investigator',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='knowninstitution',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='knowninstitution',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='knownlocation',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='knownperson',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='knownperson',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='localization',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='localization',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='location',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='location',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='partof',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='partof',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='person',
            name='validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='person',
            name='validated_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_affiliations', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_attendances', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='course',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_courses', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_coursegroups', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='institution',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_institutions', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='investigator',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_investigators', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='knowninstitution',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_known_institutions', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='knownlocation',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_known_locations', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='knownperson',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_known_persons', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='localization',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_localizations', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='location',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_locations', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='partof',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_part_of', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='person',
            name='changed_by',
            field=models.ForeignKey(related_name='edited_persons', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
    ]
