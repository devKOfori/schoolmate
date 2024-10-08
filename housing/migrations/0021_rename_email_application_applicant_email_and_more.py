# Generated by Django 5.0.2 on 2024-08-18 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0020_alter_housingoffer_room_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='email',
            new_name='applicant_email',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='tenant_name',
            new_name='applicant_name',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='phone',
            new_name='applicant_phone',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='application_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='hostels',
            new_name='selected_hostels',
        ),
    ]
