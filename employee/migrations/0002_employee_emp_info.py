# Generated by Django 5.0.2 on 2024-04-01 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emp_info',
            field=models.CharField(default='', max_length=255),
        ),
    ]