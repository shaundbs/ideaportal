# Generated by Django 3.2.5 on 2021-07-30 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_ideas_estimated_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideas',
            name='notes',
            field=models.TextField(default='Type content here...', max_length=500),
        ),
    ]
