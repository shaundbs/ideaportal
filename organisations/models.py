from django.db import models
from challenges.models import Department
from django.utils.text import slugify 
from django.templatetags.static import static
import random

# Create your models here.
health = ['heatlh1.jpg','heatlh2.jpg','heatlh3.jpg','heatlh4.jpg',]
culture = ['culture01.jpg','culture02.jpg','culture03.jpg']
data = ['data01.jpg','data02.jpg','data03.jpg','data04.jpg',]
job_satisfaction = ['job satisfaction 01.jpg','job satisfaction 02.jpg','job satisfaction 03.jpg']
relationships = ['relationship01.jpg','relationship02.jpg','relationship03.jpg','relationship04.jpg',]
leadership = ['leadership01.jpeg', 'leadership02.jpg']


class Organisation(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=200, null=True, default='none')
    is_active = models.BooleanField(max_length=50, null=True, blank=True)
    specialty = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='specialty', null=True, blank=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,)
    post1 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag1', null=True, blank=True)
    post2 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag2', null=True, blank=True)
    post3 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag3', null=True, blank=True)
    default_pic_mapping = { 'Health': random.choice(health), 'Culture': random.choice(culture), 'Job Satisfaction': random.choice(job_satisfaction),'Relationships': random.choice(relationships), 'Leadership': random.choice(leadership)}

    OPTIONS = [
    ('Health', 'Health'),
    ('Culture', 'Culture'),
    ('Job Satisfaction', 'Job Satisfaction'),
    ('Relationships', 'Relationships'),
    ('Leadership', 'Leadership'),
    ('Data', 'Data'),
    ('Other', 'Other')
    ]
    section1 = models.CharField(max_length=100, null=True, blank=True)
    section2 = models.CharField(max_length=100, null=True, blank=True)
    section3 = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=100, null=True, blank=True)

    def get_profile_pic_url(self):
        if not self.image:
            return self.default_pic_mapping[self.specialty.department]
        return self.image.url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.image = self.get_profile_pic_url()
        super(Organisation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name