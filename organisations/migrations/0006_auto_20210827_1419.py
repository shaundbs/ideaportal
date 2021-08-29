# Generated by Django 3.2.5 on 2021-08-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0005_auto_20210827_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='about',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='section1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='section2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='section3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
