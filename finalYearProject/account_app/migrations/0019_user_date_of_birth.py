# Generated by Django 4.0 on 2022-01-27 04:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0018_doctor_age_user_middle_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2022, 1, 27, 10, 16, 23, 134532)),
            preserve_default=False,
        ),
    ]
