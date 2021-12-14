# Generated by Django 3.2.5 on 2021-08-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0024_auto_20210804_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('Health', 'Health'), ('Culture', 'Culture'), ('Job Satisfaction', 'Job Satisfaction'), ('Relationships', 'Relationships'), ('Leadership', 'Leadership'), ('Data', 'Data'), ('Other', 'Other')], default='low', max_length=32)),
                ('sub_department', models.CharField(choices=[('Health', 'Health'), ('Culture', 'Culture'), ('Job Satisfaction', 'Job Satisfaction'), ('Relationships', 'Relationships'), ('Leadership', 'Leadership'), ('Data', 'Data'), ('Other', 'Other')], default='low', max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='department',
            field=models.ForeignKey(null=True, on_delete=models.SET('Dept not found'), related_name='challenge_department', to='challenges.department'),
        ),
    ]
