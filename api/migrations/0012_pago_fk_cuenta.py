# Generated by Django 3.2.4 on 2023-11-06 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_nombre_deuda_pago_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='fk_cuenta',
            field=models.ForeignKey(db_column='fk_cuenta', default=None, on_delete=django.db.models.deletion.CASCADE, to='api.tarjeta'),
        ),
    ]
