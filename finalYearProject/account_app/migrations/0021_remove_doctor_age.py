# Generated by Django 4.0 on 2022-01-27 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0020_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='age',
        ),
    ]
