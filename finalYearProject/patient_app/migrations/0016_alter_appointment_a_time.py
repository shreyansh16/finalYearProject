# Generated by Django 4.0 on 2022-01-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0015_appointment_is_marked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='a_time',
            field=models.CharField(choices=[('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00')], max_length=10),
        ),
    ]
