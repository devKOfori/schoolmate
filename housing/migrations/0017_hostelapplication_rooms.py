# Generated by Django 5.0.2 on 2024-04-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0016_roomcategory_hostelapplication_room_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostelapplication',
            name='rooms',
            field=models.ManyToManyField(to='housing.room'),
        ),
    ]