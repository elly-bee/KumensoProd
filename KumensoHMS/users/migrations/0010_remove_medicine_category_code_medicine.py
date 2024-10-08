# Generated by Django 5.0.6 on 2024-06-06 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_medicine_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine_category',
            name='code',
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('days', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('instruction', models.TextField(blank=True, null=True)),
                ('advice', models.TextField(blank=True, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.medicine_category')),
            ],
        ),
    ]
