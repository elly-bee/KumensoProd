# Generated by Django 5.0.6 on 2024-06-17 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_company_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='town',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
