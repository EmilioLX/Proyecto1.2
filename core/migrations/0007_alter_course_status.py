# Generated by Django 4.2.6 on 2023-10-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_course_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('Prog', 'En progreso'), ('insc', 'Etapa de inscripcion'), ('fina', 'Finalizado')], default='insc', max_length=4, verbose_name='Estado'),
        ),
    ]
