# Generated by Django 4.2.6 on 2023-10-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='schedule',
            field=models.PositiveIntegerField(default=0, verbose_name='horario'),
        ),
    ]
