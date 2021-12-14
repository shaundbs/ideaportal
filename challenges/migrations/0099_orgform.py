# Generated by Django 3.2.5 on 2021-09-15 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0021_delete_orgform'),
        ('blog', '0082_alter_comment_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0098_alter_department_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=' ', error_messages={'unique': 'Idea title is too similar to an existing one'}, max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('estimated_cost', models.DecimalField(blank=True, decimal_places=2, default=300, max_digits=6, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(error_messages={'unique': 'Idea description is too similar to an existing one'}, max_length=500, unique=True)),
                ('notes', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('is_user_led', models.BooleanField(default=True)),
                ('is_similar', models.BooleanField(default=False, null=True)),
                ('is_approved', models.BooleanField(default=False, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/idea_images')),
                ('stage', models.CharField(blank=True, choices=[('open', 'Open'), ('under review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('in development', 'In development'), ('delivered', 'Delivered')], max_length=2000, null=True)),
                ('field_1', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_2', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_3', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_4', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_5', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_6', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_7', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_8', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_9', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_10', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_11', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_12', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_13', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_14', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_15', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_16', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_17', models.BooleanField(blank=True, default=None, max_length=50, null=True)),
                ('field_2_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_3_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_4_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_5_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_6_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_7_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_8_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_9_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_1_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_11_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_12_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_13_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_14_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_15_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_16_name', models.CharField(blank=True, max_length=32, null=True)),
                ('field_17_name', models.CharField(blank=True, max_length=32, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orgform_author', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orgform_department', to='challenges.department')),
                ('likes', models.ManyToManyField(related_name='orgform_likes', to=settings.AUTH_USER_MODEL)),
                ('org_tag', models.ManyToManyField(null=True, related_name='orgform_orgtag', to='organisations.Organisation')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orgform_ideas', to='blog.post')),
                ('sub_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orgform_sub_department', to='challenges.department')),
            ],
        ),
    ]
