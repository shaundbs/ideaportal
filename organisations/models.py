from django.db import models
from challenges.models import Department
from django.utils.text import slugify 

# Create your models here.


class Organisation(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=200, null=True, default='none')
    is_active = models.BooleanField(max_length=50, null=True, blank=True)
    specialty = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='specialty', null=True, blank=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    post1 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag1', null=True, blank=True)
    post2 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag2', null=True, blank=True)
    post3 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag3', null=True, blank=True)
    section1 = models.CharField(max_length=100, null=True, blank=True)
    section2 = models.CharField(max_length=100, null=True, blank=True)
    section3 = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Organisation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name