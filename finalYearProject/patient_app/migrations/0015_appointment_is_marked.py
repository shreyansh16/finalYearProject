# Generated by Django 4.0 on 2021-12-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0014_appointment_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_marked',
            field=models.BooleanField(default=False),
        ),
    ]
