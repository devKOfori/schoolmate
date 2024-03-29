# Generated by Django 5.0.2 on 2024-03-25 01:29

import django.db.models.deletion
import housing.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_created_by'),
        ('housing', '0016_room_created_at_room_created_by_roomrequest_tenant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifyproperty',
            name='attachment',
            field=models.FileField(upload_to=housing.models.upload_to, verbose_name='Attach Document'),
        ),
    ]
