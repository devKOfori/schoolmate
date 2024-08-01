# Generated by Django 5.0.2 on 2024-07-03 16:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=6)),
            ],
            options={
                'verbose_name_plural': 'Genders',
                'db_table': 'gender',
            },
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Marital Statusses',
                'db_table': 'maritalstatus',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Nationalities',
                'db_table': 'nationality',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Region',
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Relations',
                'db_table': 'relation',
            },
        ),
    ]