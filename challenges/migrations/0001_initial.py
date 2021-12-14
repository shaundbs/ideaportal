# Generated by Django 3.2.5 on 2021-07-25 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('field', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('severity', models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high'), ('urgent', 'urgent')], default='low', max_length=32)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(default='Type content here...', max_length=500)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_author', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_manager', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(default=None, on_delete=models.SET('User not found'), related_name='challenge_winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
