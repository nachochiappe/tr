# Generated by Django 2.0.2 on 2018-03-18 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0011_auto_20180218_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamento',
            name='dosis_a_tomar',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
