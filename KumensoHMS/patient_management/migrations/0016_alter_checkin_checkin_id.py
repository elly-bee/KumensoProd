# Generated by Django 5.0.6 on 2024-06-06 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0015_checkin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='checkin_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
