from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from account.models import Account
from blog.models import Post
import ideaportal.settings as settings
from django.utils.text import slugify 
from django.db.models import Count, Max
import random
import logging

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
    ('Custom', 'Custom'),
    ('Other', 'Other'),
    ]
    department = models.CharField(max_length=32, choices=OPTIONS, default='Other')
    sub_department = models.CharField(max_length=50, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)

    class Meta:
        unique_together = ("department", "sub_department")


    def __str__(self):
        return self.department


class Challenge(models.Model):
    title = models.CharField(max_length=200, unique=True, error_messages={'unique':"A challenge with this title already exists"})
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='challenge_author', null=True)
    SEVERITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]
    severity = models.CharField(max_length=32, choices=SEVERITY_CHOICES, default='low')
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,default='',  unique=True, error_messages={'unique':"This challenge is too similar to an existing one"})
    created_on = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=CASCADE, related_name='category', null=True)
    anonymous = models.BooleanField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/challenge_images_lib")
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
    
    title = models.CharField(max_length=200, unique=True, default=" ", error_messages={'unique':"Idea title is too similar to an existing one"})
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ideas', null=True)
    slug = models.SlugField(max_length=200, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='idea_author', null=True)
    estimated_cost = models.DecimalField(max_digits=6, decimal_places=2, default=300, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,unique=True, error_messages={'unique':"Idea description is too similar to an existing one"})
    notes = models.TextField(max_length=500,default='', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_user_led = models.BooleanField(default=True)
    is_similar = models.BooleanField(default=False, null=True)
    is_approved = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/idea_images")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_department', null=True, blank=True)
    sub_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_sub_department', null=True, blank=True)
    likes = models.ManyToManyField(Account, related_name='idea_likes', null=True, blank=True)
    is_pridar = models.BooleanField(default=False)
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
        logging.error(self.winner)
        super(Idea, self).save(*args, **kwargs)


class IdeaComment(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='idea_comment_author', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='idea_comment_likes', blank=True)
    image = models.ImageField(null=True, blank=True,)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments', default=0, null=True, blank=True)
        
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.comment

class OrgForm(models.Model):
    title = models.CharField(max_length=200, unique=True, default=" ", error_messages={'unique':"Idea title is too similar to an existing one"}, null=True, blank=True)
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name='orgform_ideas', null=True)
    slug = models.SlugField(max_length=200, null=True)
    author = models.ForeignKey("account.Account", on_delete=models.CASCADE, related_name='orgform_author', null=True)
    estimated_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,unique=True, error_messages={'unique':"Idea description is too similar to an existing one"}, null=True, blank=True)
    notes = models.TextField(max_length=500,default='', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_user_led = models.BooleanField(default=True)
    is_similar = models.BooleanField(default=False, null=True)
    is_approved = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/idea_images")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='orgform_department', null=True, blank=True)
    sub_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='orgform_sub_department', null=True, blank=True)
    likes = models.ManyToManyField("account.Account", related_name='orgform_likes')
    STAGES = [
    ('open', 'Open'),
    ('under review', 'Under Review'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('in development', 'In development'),
    ('delivered', 'Delivered'),
]
    stage = models.CharField(max_length=2000, choices=STAGES, blank=True, null=True)
    org_tag = models.ManyToManyField("organisations.Organisation", related_name='orgform_orgtag', null=True)

    in_sandbox = models.BooleanField(default=False)
    is_released_and_supported = models.BooleanField(default=False)
    is_open_source_partnership = models.BooleanField(default=False)
    NICE_Tier1_DTAC_evidence_in_place = models.BooleanField(default=False)
    NICE_Tier2_DTAC_evidence_in_place = models.BooleanField(default=False)
    risk_and_mitigations_are_public = models.BooleanField(default=False)
    ce_mark_dcb_register = models.BooleanField(default=False)
    safety_officer_stated = models.BooleanField(default=False)
    iso_supplier = models.BooleanField(default=False)
    user_kpis_is_an_ai_pathway_are_defined = models.BooleanField(default=False)
    user_to_board_approval_obtained = models.BooleanField(default=False)
    cost_of_dev_and_support_agreed = models.BooleanField(default=False)
    ip_agreement_in_place = models.BooleanField(default=False)
    ig_agreements_in_place = models.BooleanField(default=False)
    data_and_model_agreed = models.BooleanField(default=False)
    
    field_16 = models.BooleanField(default=False)
    field_17 = models.BooleanField(default=False)
    field_1_name = models.CharField(max_length=32, null=True, blank=True)
    field_2_name= models.CharField(max_length=32, null=True, blank=True)
    field_3_name = models.CharField(max_length=32, null=True, blank=True)
    field_4_name = models.CharField(max_length=32, null=True, blank=True)
    field_5_name = models.CharField(max_length=32, null=True, blank=True)
    field_6_name = models.CharField(max_length=32, null=True, blank=True)
    field_7_name = models.CharField(max_length=32, null=True, blank=True)
    field_8_name = models.CharField(max_length=32, null=True, blank=True)
    field_9_name = models.CharField(max_length=32, null=True, blank=True)
    field_1_name = models.CharField(max_length=32, null=True, blank=True)
    field_11_name = models.CharField(max_length=32, null=True, blank=True)
    field_12_name = models.CharField(max_length=32, null=True, blank=True)
    field_13_name = models.CharField(max_length=32, null=True, blank=True)
    field_14_name = models.CharField(max_length=32, null=True, blank=True)
    field_15_name = models.CharField(max_length=32, null=True, blank=True)
    field_16_name = models.CharField(max_length=32, null=True, blank=True)
    field_17_name = models.CharField(max_length=32, null=True, blank=True)


    def __str__(self):
        return str(self.title)

    def total_likes(self):
        return self.likes.count()

    def total_likes(self):
        return self.likes.count()

    def total_likes_received(user):
        return user.idea_author.aggregate(total_likes=Count('likes'))['total_likes'] or 0

    def total_ideas_selected(user):
        return user.idea_author.aggregate(total_wins=Count('winner'))['total_wins'] or 0

    def total_likes_given(user):
        return user.idea_likes.count()

    def favourite_department(user):
        return user.idea_department.count()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(OrgForm, self).save(*args, **kwargs)