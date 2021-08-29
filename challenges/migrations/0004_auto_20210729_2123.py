# Generated by Django 3.2.5 on 2021-07-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_auto_20210725_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenges',
            name='image',
            field=models.ImageField(default='images/genger.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='ideas',
            name='image',
            field=models.ImageField(default='images/genger.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='ideas',
            name='title',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
