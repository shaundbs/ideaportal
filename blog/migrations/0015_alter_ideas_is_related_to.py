# Generated by Django 3.2.5 on 2021-08-01 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_ideas_is_related_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideas',
            name='is_related_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
