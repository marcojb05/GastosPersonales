# Generated by Django 4.2.5 on 2023-09-13 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alumno_has_genero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumno_has_genero',
            name='id',
        ),
        migrations.AddField(
            model_name='alumno_has_genero',
            name='idAlumno_has_genero',
            field=models.AutoField(db_column='idAlumno_has_genero', default=1, primary_key=True, serialize=False),
        ),
    ]
