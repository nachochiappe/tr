# Generated by Django 2.0 on 2017-12-10 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0002_auto_20171208_1458'),
        ('pacientes', '0006_paciente_medico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudio', models.CharField(max_length=100)),
                ('fecha_solicitud', models.DateField()),
                ('fecha_completado', models.DateField()),
                ('estado', models.CharField(max_length=20)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicos.Medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pacientes.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamento', models.CharField(max_length=50)),
                ('posologia', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('dosis_completadas', models.PositiveIntegerField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicos.Medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pacientes.Paciente')),
            ],
        ),
    ]