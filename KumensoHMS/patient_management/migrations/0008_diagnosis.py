# Generated by Django 5.0.6 on 2024-05-31 10:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0007_alter_vitals_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.healthcondition')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.patient')),
            ],
        ),
    ]
