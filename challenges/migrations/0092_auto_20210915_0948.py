# Generated by Django 3.2.5 on 2021-09-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0091_auto_20210915_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='description',
            field=models.TextField(error_messages={'unique': 'A challenge with this title already exists'}, max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.CharField(default=' ', error_messages={'unique': 'A challenge with this title already exists'}, max_length=200, unique=True),
        ),
    ]
