# Generated by Django 4.0 on 2021-12-28 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0015_doctor_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='doctor_reg_id',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
