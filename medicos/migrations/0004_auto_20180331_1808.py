# Generated by Django 2.0.2 on 2018-03-31 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0003_medico_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medico',
            old_name='dni',
            new_name='documento',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='nombre',
        ),
    ]
