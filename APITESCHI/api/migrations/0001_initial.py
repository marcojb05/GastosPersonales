# Generated by Django 4.2.5 on 2023-10-04 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTransaccion',
            fields=[
                ('id_tipo', models.IntegerField(db_column='id_tipo', primary_key=True, serialize=False)),
                ('tipo_transaccion', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'TipoTransaccion',
            },
        ),
    ]
