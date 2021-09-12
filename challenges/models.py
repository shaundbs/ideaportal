from django.db import models
from django.db.models.deletion import SET_NULL
from account.models import Account
from blog.models import Post
import ideaportal.settings as settings
from django.utils.text import slugify 
from django.db.models import Count, Max
import random

# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

BOOLEAN = (
    (0,"Draft"),
    (1,"Publish")
)

health = ['heatlh1.jpg','heatlh2.jpg','heatlh3.jpg','heatlh4.jpg',]
culture = ['culture01.jpg','culture02.jpg','culture03.jpg']
data = ['data01.jpg','data02.jpg','data03.jpg','data04.jpg',]
job_satisfaction = ['job satisfaction 01.jpg','job satisfaction 02.jpg','job satisfaction 03.jpg']
relationships = ['relationship01.jpg','relationship02.jpg','relationship03.jpg','relationship04.jpg',]
leadership = ['leadership01.jpeg', 'leadership02.jpg']

class Department(models.Model):
    OPTIONS = [
    ('Health', 'Health'),
    ('Culture', 'Culture'),
    ('Job Satisfaction', 'Job Satisfaction'),
    ('Relationships', 'Relationships'),
    ('Leadership', 'Leadership'),
    ('Data', 'Data'),
    ('Other', 'Other')
    ]
    department = models.CharField(max_length=32, choices=OPTIONS, default='Other')
    sub_department = models.CharField(max_length=50, unique=True, null=True, blank=True )
    is_approved = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)

    class Meta:
        unique_together = ("department", "sub_department")


    def __str__(self):
        return self.department


class Challenge(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='challenge_author', null=True)
    SEVERITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]
    severity = models.CharField(max_length=32, choices=SEVERITY_CHOICES, default='low')
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='category', null=True)
    image = models.ImageField(null=True, blank=True)
    org_tag = models.ForeignKey("organisations.Organisation", on_delete=models.SET_NULL, related_name='challengeorgtag', null=True)
    default_pic_mapping = { 'Health': random.choice(health), 'Culture': random.choice(culture), 'Job Satisfaction': random.choice(job_satisfaction),'Relationships': random.choice(relationships), 'Leadership': random.choice(leadership),  'Data': random.choice(data)}

    def get_profile_pic_url(self):
        if not self.image:
            return self.default_pic_mapping[self.department.department]
        return self.image

    def save(self, *args, **kwargs):
        self.image = self.get_profile_pic_url()
        super(Challenge, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class Idea(models.Model):
    
    title = models.CharField(max_length=200, unique=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ideas', null=True)
    slug = models.SlugField(max_length=200, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='idea_author', null=True)
    estimated_cost = models.DecimalField(max_digits=6, decimal_places=2, default=300, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,default='')
    notes = models.TextField(max_length=500,default='', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_user_led = models.BooleanField(default=True)
    is_similar = models.BooleanField(default=False, null=True)
    is_approved = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/idea_images")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_department', null=True, blank=True)
    sub_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_sub_department', null=True, blank=True)
    likes = models.ManyToManyField(Account, related_name='idea_likes')
    STAGES = [
    ('open', 'Open'),
    ('under review', 'Under Review'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('in development', 'In development'),
    ('delivered', 'Delivered'),
]
    stage = models.CharField(max_length=2000, choices=STAGES, blank=True, null=True)
    org_tag = models.ManyToManyField("organisations.Organisation", related_name='ideaorgtag', null=True)

    def __str__(self):
        return str(self.title)

    def total_likes(self):
        return self.likes.count()

    def total_likes(self):
        return self.likes.count()

    # def get_winner(self, challenge):
    #     return self.likes.count(max)

    # def get_winner(post):
    #     return post.id(post.)

    def total_likes_received(user):
        return user.idea_author.aggregate(total_likes=Count('likes'))['total_likes'] or 0

    def total_ideas_selected(user):
        return user.idea_author.aggregate(total_wins=Count('winner'))['total_wins'] or 0

    def total_likes_given(user):
        return user.idea_likes.count()

    # def favourite_org(user):
    #     return user.idea_department.count(Max).title

    def favourite_department(user):
        return user.idea_department.count()

    # def __str__(self):
    #     return "£ " + str(self.estimated_cost)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.winner = self.get_winner()
        print(self.winner)
        super(Idea, self).save(*args, **kwargs)


class IdeaComment(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='idea_comment_author', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500,default='Type content here...')
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='idea_comment_likes', blank=True)
    image = models.ImageField(upload_to='images/', default='images/gender.png', null=True, blank=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments', default=0, null=True, blank=True)
        
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.comment

# class Custom(models.Model):
#     organisation = models.ForeignKey("organisations.Organisation", on_delete=models.SET_NULL, related_name='idea_comment_author', null=True)
#     creator = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='idea_comment_author', null=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     field_1 = models.TextField(max_length=500,default='Type content here...')
#     field_2= models.TextField(max_length=500,default='Type content here...')
#     field_3 = models.TextField(max_length=500,default='Type content here...')
#     field_4 = models.TextField(max_length=500,default='Type content here...')
#     field_5 = models.TextField(max_length=500,default='Type content here...')
#     field_6 = models.TextField(max_length=500,default='Type content here...')
#     field_7 = models.TextField(max_length=500,default='Type content here...')
#     field_8 = models.TextField(max_length=500,default='Type content here...')
#     field_9 = models.TextField(max_length=500,default='Type content here...')
#     field_10 = models.TextField(max_length=500,default='Type content here...')
#     field_11 = models.TextField(max_length=500,default='Type content here...')
#     field_12 = models.TextField(max_length=500,default='Type content here...')
#     field_13 = models.TextField(max_length=500,default='Type content here...')
#     field_14 = models.TextField(max_length=500,default='Type content here...')
#     field_15 = models.TextField(max_length=500,default='Type content here...')
#     field_16 = models.TextField(max_length=500,default='Type content here...')
#     field_17 = models.TextField(max_length=500,default='Type content here...')
