# Generated by Django 3.2.4 on 2023-11-06 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_pago_nombre_deuda'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='nombre_deuda',
            new_name='titulo',
        ),
    ]
