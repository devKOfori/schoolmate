# Generated by Django 5.0.2 on 2024-07-26 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0008_alter_rooms_floor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='hostel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='housing.hostels'),
        ),
    ]
