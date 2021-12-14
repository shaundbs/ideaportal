# Generated by Django 3.2.5 on 2021-08-27 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0004_organisation_image'),
        ('challenges', '0078_alter_challenge_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='org_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challengeorgtag', to='organisations.organisation'),
        ),
        migrations.AddField(
            model_name='idea',
            name='org_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ideaorgtag', to='organisations.organisation'),
        ),
    ]
