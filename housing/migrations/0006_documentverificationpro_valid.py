# Generated by Django 5.0.2 on 2024-03-30 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0005_badge_valid_verifyproperty_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentverificationpro',
            name='valid',
            field=models.BooleanField(default=True),
        ),
    ]