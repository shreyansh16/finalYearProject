# Generated by Django 4.0 on 2021-12-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0002_alter_appointment_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='a_time',
            field=models.CharField(choices=[('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00')], max_length=10),
        ),
    ]
