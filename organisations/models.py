from django.db import models
from challenges.models import Department
from django.utils.text import slugify 
from django.templatetags.static import static
import random
from django.db.models import Count, Max

# Create your models here.
health = ['heatlh1.jpg','heatlh2.jpg','heatlh3.jpg','heatlh4.jpg',]
culture = ['culture01.jpg','culture02.jpg','culture03.jpg']
data = ['data01.jpg','data02.jpg','data03.jpg','data04.jpg',]
job_satisfaction = ['job satisfaction 01.jpg','job satisfaction 02.jpg','job satisfaction 03.jpg']
relationships = ['relationship01.jpg','relationship02.jpg','relationship03.jpg','relationship04.jpg',]
leadership = ['leadership01.jpeg', 'leadership02.jpg']

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Organisation(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=200, null=True, default='none')
    is_active = models.BooleanField(max_length=50, null=True, blank=True)
    specialty = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='specialty', null=True, blank=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,)
    post1 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag1', null=True, blank=True)
    post2 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag2', null=True, blank=True)
    post3 = models.ForeignKey("blog.Post", on_delete=models.SET_NULL, related_name='postorgtag3', null=True, blank=True)
    default_pic_mapping = { 'Health': random.choice(health), 'Culture': random.choice(culture), 'Job Satisfaction': random.choice(job_satisfaction),'Relationships': random.choice(relationships), 'Leadership': random.choice(leadership)}
    api_on = models.BooleanField(max_length=50,  default=True)
    custom_form_on = models.BooleanField(max_length=50,  default=False)


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
        return self.image

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.image = self.get_profile_pic_url()
        super(Organisation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class OrgForm(models.Model):
#     title = models.CharField(max_length=200, unique=True, default=" ", error_messages={'unique':"Idea title is too similar to an existing one"})
#     post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name='orgform_ideas', null=True)
#     slug = models.SlugField(max_length=200, null=True)
#     author = models.ForeignKey("account.Account", on_delete=models.CASCADE, related_name='orgform_author', null=True)
#     estimated_cost = models.DecimalField(max_digits=6, decimal_places=2, default=300, blank=True, null=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     description = models.TextField(max_length=500,unique=True, error_messages={'unique':"Idea description is too similar to an existing one"})
#     notes = models.TextField(max_length=500,default='', null=True, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.IntegerField(choices=STATUS, default=0)
#     is_user_led = models.BooleanField(default=True)
#     is_similar = models.BooleanField(default=False, null=True)
#     is_approved = models.BooleanField(default=False, null=True)
#     image = models.ImageField(null=True, blank=True, upload_to="images/idea_images")
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='orgform_department', null=True, blank=True)
#     sub_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='orgform_sub_department', null=True, blank=True)
#     likes = models.ManyToManyField("account.Account", related_name='orgform_likes')
#     STAGES = [
#     ('open', 'Open'),
#     ('under review', 'Under Review'),
#     ('accepted', 'Accepted'),
#     ('rejected', 'Rejected'),
#     ('in development', 'In development'),
#     ('delivered', 'Delivered'),
# ]
#     stage = models.CharField(max_length=2000, choices=STAGES, blank=True, null=True)
#     org_tag = models.ManyToManyField("organisations.Organisation", related_name='orgform_orgtag', null=True)

#     field_1 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_2= models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_3 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_4 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_5 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_6 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_7 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_8 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_9 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_10 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_11 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_12 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_13 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_14 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_15 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_16 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_17 = models.BooleanField(max_length=50,  default=None, null=True, blank=True)
#     field_1_name = models.CharField(max_length=32, null=True, blank=True)
#     field_2_name= models.CharField(max_length=32, null=True, blank=True)
#     field_3_name = models.CharField(max_length=32, null=True, blank=True)
#     field_4_name = models.CharField(max_length=32, null=True, blank=True)
#     field_5_name = models.CharField(max_length=32, null=True, blank=True)
#     field_6_name = models.CharField(max_length=32, null=True, blank=True)
#     field_7_name = models.CharField(max_length=32, null=True, blank=True)
#     field_8_name = models.CharField(max_length=32, null=True, blank=True)
#     field_9_name = models.CharField(max_length=32, null=True, blank=True)
#     field_1_name = models.CharField(max_length=32, null=True, blank=True)
#     field_11_name = models.CharField(max_length=32, null=True, blank=True)
#     field_12_name = models.CharField(max_length=32, null=True, blank=True)
#     field_13_name = models.CharField(max_length=32, null=True, blank=True)
#     field_14_name = models.CharField(max_length=32, null=True, blank=True)
#     field_15_name = models.CharField(max_length=32, null=True, blank=True)
#     field_16_name = models.CharField(max_length=32, null=True, blank=True)
#     field_17_name = models.CharField(max_length=32, null=True, blank=True)


#     def __str__(self):
#         return str(self.title)

#     def total_likes(self):
#         return self.likes.count()

#     def total_likes(self):
#         return self.likes.count()

#     def total_likes_received(user):
#         return user.idea_author.aggregate(total_likes=Count('likes'))['total_likes'] or 0

#     def total_ideas_selected(user):
#         return user.idea_author.aggregate(total_wins=Count('winner'))['total_wins'] or 0

#     def total_likes_given(user):
#         return user.idea_likes.count()


#     def favourite_department(user):
#         return user.idea_department.count()


#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         print(self.winner)
#         super(OrgForm, self).save(*args, **kwargs)