# Generated by Django 4.0 on 2022-01-27 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0022_doctor_unique_doctor_reg_id'),
        ('patient_app', '0017_alter_appointment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.patient'),
        ),
        migrations.CreateModel(
            name='DocumentUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=120)),
                ('document_name', models.CharField(max_length=120)),
                ('document', models.FileField(blank=True, null=True, upload_to='documentUpload/')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.patient')),
            ],
        ),
    ]
