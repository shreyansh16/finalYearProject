# Generated by Django 4.0 on 2021-12-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0013_user_header_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='likes',
            field=models.ManyToManyField(related_name='doctor_likes', to='account_app.Patient'),
        ),
    ]
