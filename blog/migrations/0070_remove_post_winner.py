# Generated by Django 3.2.5 on 2021-08-13 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0069_alter_post_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='winner',
        ),
    ]
