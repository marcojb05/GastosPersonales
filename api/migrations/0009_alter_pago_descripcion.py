# Generated by Django 3.2.4 on 2023-11-06 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_encuesta_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='descripcion',
            field=models.TextField(max_length=255),
        ),
    ]
