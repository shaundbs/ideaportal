# Generated by Django 3.2.5 on 2021-08-04 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0031_auto_20210804_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='sub_department',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
