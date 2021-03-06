# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_auto_20171111_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='fecnac',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paciente',
            name='mail',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
    ]
