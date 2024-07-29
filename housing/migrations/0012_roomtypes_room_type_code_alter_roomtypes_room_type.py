# Generated by Django 5.0.2 on 2024-07-27 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0011_alter_hostelamenities_amenity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtypes',
            name='room_type_code',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='roomtypes',
            name='room_type',
            field=models.CharField(max_length=255, unique=True, verbose_name='Room Type'),
        ),
    ]
