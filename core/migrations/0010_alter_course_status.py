# Generated by Django 4.2.6 on 2023-10-18 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_course_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('I', 'Inscripciones'), ('P', 'En progreso'), ('F', 'Finalizado')], default='I', max_length=1, verbose_name='Estado'),
        ),
    ]