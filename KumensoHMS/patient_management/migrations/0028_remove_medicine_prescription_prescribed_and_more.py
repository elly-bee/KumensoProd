# Generated by Django 5.0.6 on 2024-06-12 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0027_remove_checkin_medication_checkin_medication'),
        ('users', '0015_rename_costdef_services_disc_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine_prescription',
            name='prescribed',
        ),
        migrations.AddField(
            model_name='medicine_prescription',
            name='prescribed_id',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='users.inventory_list'),
            preserve_default=False,
        ),
    ]
