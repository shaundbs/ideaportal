# Generated by Django 3.2.5 on 2021-08-09 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0047_alter_idea_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
