# Generated by Django 4.0 on 2021-12-16 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0011_doctor_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='degrees',
            field=models.CharField(default='No degrees Specified', max_length=250),
        ),
    ]
