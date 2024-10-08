# Generated by Django 5.0.6 on 2024-06-06 13:42

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_management', '0012_rename_name_medicine_prescription_drug_name'),
        ('users', '0013_rename_name_medicine_drug_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateTimeField(default=datetime.datetime.today)),
                ('checkout_date', models.DateTimeField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department')),
                ('diagnosis', models.ManyToManyField(to='patient_management.diagnosis')),
                ('medication', models.ManyToManyField(to='users.medicine')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_management.patient')),
                ('service', models.ManyToManyField(to='users.services')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vitals', models.ManyToManyField(to='patient_management.vitals')),
            ],
        ),
    ]
