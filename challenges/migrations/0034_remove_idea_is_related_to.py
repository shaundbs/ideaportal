# Generated by Django 3.2.5 on 2021-08-04 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0033_auto_20210804_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='is_related_to',
        ),
    ]
