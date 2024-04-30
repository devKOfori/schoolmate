# Generated by Django 5.0.2 on 2024-04-04 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0012_alter_room_number_of_beds'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='room_cost_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='facility',
            name='room_cost_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='floor',
            name='room_cost_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='area',
            field=models.DecimalField(decimal_places=1, default=1.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='housing.facilitycategory'),
        ),
        migrations.AlterModelTable(
            name='facility',
            table='hostelitem',
        ),
        migrations.AlterModelTable(
            name='facilitycategory',
            table='hostelitemcategory',
        ),
    ]