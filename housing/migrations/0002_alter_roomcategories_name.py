# Generated by Django 5.0.2 on 2024-07-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomcategories',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
