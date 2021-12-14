# Generated by Django 3.2.5 on 2021-09-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0081_alter_challenge_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='stage',
            field=models.CharField(blank=True, choices=[('open', 'Open'), ('under review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('in development', 'In development'), ('delivered', 'Delivered')], max_length=2000, null=True),
        ),
    ]
