# Generated by Django 3.2.5 on 2021-08-31 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0078_auto_20210827_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='endDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='startDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
