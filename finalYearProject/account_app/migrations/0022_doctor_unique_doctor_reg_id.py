# Generated by Django 4.0 on 2022-01-27 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0021_remove_doctor_age'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='doctor',
            constraint=models.UniqueConstraint(fields=('doctor_reg_id',), name='unique_doctor_reg_id'),
        ),
    ]