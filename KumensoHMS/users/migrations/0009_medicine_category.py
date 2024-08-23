# Generated by Django 5.0.6 on 2024-06-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_inventory_list_unit_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('code', models.CharField(editable=False, max_length=10, unique=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('inactive', 'inactive')], default='Active', max_length=255)),
            ],
        ),
    ]
