# Generated by Django 3.2.5 on 2021-08-27 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_organisation_image'),
        ('blog', '0074_post_org_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='org_tag',
        ),
        migrations.AddField(
            model_name='post',
            name='org_tag',
            field=models.ManyToManyField(null=True, related_name='postorgtag', to='organisations.Organisation'),
        ),
    ]
