# Generated by Django 3.2.5 on 2021-08-03 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0015_auto_20210803_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='image',
        ),
        migrations.AlterField(
            model_name='challenge',
            name='endDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='field',
            field=models.CharField(choices=[('Health', 'Health'), ('Culture', 'Culture'), ('Job Satisfaction', 'Job Satisfaction'), ('Relationships', 'Relationships'), ('Leadership', 'Leadership'), ('Data', 'Data')], max_length=50),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='startDate',
            field=models.DateTimeField(null=True),
        ),
    ]
