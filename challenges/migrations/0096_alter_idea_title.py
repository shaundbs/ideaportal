# Generated by Django 3.2.5 on 2021-09-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0095_auto_20210915_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.CharField(default=' ', error_messages={'unique': 'Idea itle is too similar to an existing one'}, max_length=200, unique=True),
        ),
    ]
