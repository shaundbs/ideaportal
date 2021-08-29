# Generated by Django 3.2.5 on 2021-08-02 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_delete_ideas'),
        ('challenges', '0006_ideas'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideas',
            name='is_related_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_ideas', to='blog.post'),
        ),
    ]
