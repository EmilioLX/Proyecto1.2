# Generated by Django 4.2.6 on 2023-10-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_course_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('I', 'Etapa de inscripcion'), ('F', 'Finalizado'), ('P', 'En progreso')], default='I', max_length=1, verbose_name='Estado'),
        ),
    ]