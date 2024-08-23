# Generated by Django 5.0.6 on 2024-06-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0024_remove_checkin_medication_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine_prescription',
            old_name='checkin',
            new_name='checkin_record',
        ),
        migrations.AddField(
            model_name='checkin',
            name='medication',
            field=models.ManyToManyField(blank=True, related_name='checkins', to='patient_management.medicine_prescription'),
        ),
    ]
