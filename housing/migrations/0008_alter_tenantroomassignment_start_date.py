# Generated by Django 5.0.2 on 2024-02-20 00:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0007_hostelamenities_offerresponse_requeststatus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantroomassignment',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
