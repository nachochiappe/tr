# Generated by Django 2.0.2 on 2018-04-03 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administradores', '0003_administrador_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='administrador',
            old_name='dni',
            new_name='documento',
        ),
        migrations.RemoveField(
            model_name='administrador',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='administrador',
            name='nombre',
        ),
    ]