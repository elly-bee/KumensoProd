# Generated by Django 5.0.6 on 2024-06-06 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0011_medicine_prescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine_prescription',
            old_name='name',
            new_name='drug_name',
        ),
    ]
