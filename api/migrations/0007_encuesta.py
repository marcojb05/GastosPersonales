# Generated by Django 3.2.4 on 2023-11-05 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_delete_encuesta'),
    ]

    operations = [
        migrations.CreateModel(
            name='encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta1', models.TextField(db_column='Satisfacción con el sistema')),
                ('pregunta2', models.TextField(db_column='Facilidad de uso y la amigabilidad de la interfaz')),
                ('pregunta3', models.TextField(db_column='Facilidad de usar y entender')),
                ('pregunta4', models.TextField(db_column='Frecuencia de problemas técnicos o errores')),
                ('pregunta5', models.TextField(db_column='Adaptabilidad a necesidades específicas y requisitos comerciales')),
                ('pregunta6', models.TextField(db_column='Mejoras en la eficiencia')),
                ('pregunta7', models.TextField(db_column='Utilidad de informes y análisis financieros')),
                ('pregunta8', models.TextField(db_column='Capacidad para manejar múltiples divisas y tasas de cambio')),
                ('pregunta9', models.TextField(db_column='Interrupciones en el servicio')),
                ('pregunta10', models.TextField(db_column='Perdida de datos críticos o información financiera')),
            ],
            options={
                'db_table': 'api_encuesta',
            },
        ),
    ]
