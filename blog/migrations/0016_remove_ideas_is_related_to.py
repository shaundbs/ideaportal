# Generated by Django 3.2.5 on 2021-08-01 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_ideas_is_related_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ideas',
            name='is_related_to',
        ),
    ]
