# Generated by Django 5.0.6 on 2024-07-10 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0029_alter_medicine_prescription_quantity'),
        ('users', '0019_company_town'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='status',
            field=models.CharField(choices=[('Checked in', 'Checked in'), ('Collect Vitals', 'Collect Vitals'), ('Perform diagnosis', 'Perform diagnosis'), ('Prescription', 'Prescription'), ('Complete', 'Complete')], default='Checked in', max_length=50),
        ),
    ]
