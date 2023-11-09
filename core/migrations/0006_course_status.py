# Generated by Django 4.2.6 on 2023-10-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_course_cost_alter_course_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('fina', 'Finalizado'), ('Prog', 'En progreso'), ('insc', 'Etapa de inscripcion')], default='insc', max_length=4, verbose_name='Estado'),
        ),
    ]
