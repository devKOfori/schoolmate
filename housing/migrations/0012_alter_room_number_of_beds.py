# Generated by Django 5.0.2 on 2024-04-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0011_alter_room_occupancy_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number_of_beds',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]