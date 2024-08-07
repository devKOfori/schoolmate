# Generated by Django 5.0.2 on 2024-07-28 16:17

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0013_alter_hostels_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Application ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Application Code')),
                ('tenant_name', models.CharField(max_length=255, verbose_name='Name of Applicant')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=255, verbose_name='Name of Applicant')),
                ('application_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Application Date')),
            ],
            options={
                'verbose_name': 'hostel Application',
                'verbose_name_plural': 'hostel Applications',
                'db_table': 'applications',
            },
        ),
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Status ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'application Status',
                'verbose_name_plural': 'application Statuses',
                'db_table': 'applicationstatus',
            },
        ),
        migrations.CreateModel(
            name='ApplicationHostel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Application ID')),
                ('code', models.CharField(max_length=50, verbose_name='Application Code')),
                ('application_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housing.application', verbose_name='applications')),
                ('hostel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housing.hostels', verbose_name='hostels')),
                ('room_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='housing.roomtypes', verbose_name='room types')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='housing.applicationstatus', verbose_name='status')),
            ],
            options={
                'verbose_name': 'application Hostel',
                'verbose_name_plural': 'applications Hostels',
                'db_table': 'applicationhostel',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='hostels',
            field=models.ManyToManyField(related_name='applications', through='housing.ApplicationHostel', to='housing.hostels', verbose_name='hostels'),
        ),
    ]
