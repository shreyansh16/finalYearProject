# Generated by Django 4.0 on 2022-01-27 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0019_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]