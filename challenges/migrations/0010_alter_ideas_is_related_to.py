# Generated by Django 3.2.5 on 2021-08-02 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_post_author'),
        ('challenges', '0009_alter_ideas_is_related_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideas',
            name='is_related_to',
            field=models.ForeignKey(null=True, on_delete=models.SET('Post not found'), related_name='challenge_ideas', to='blog.post'),
        ),
    ]
