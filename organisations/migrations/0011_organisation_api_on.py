# Generated by Django 3.2.5 on 2021-09-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0010_alter_organisation_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='api_on',
            field=models.BooleanField(blank=True, max_length=50, null=True),
        ),
    ]
