# Generated by Django 4.0 on 2021-12-17 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0004_alter_appointment_a_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='a_date',
            field=models.CharField(max_length=25),
        ),
    ]