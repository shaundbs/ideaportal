from django.db import models
from django.db.models.deletion import SET_NULL
from account.models import Account
from blog.models import Post
import ideaportal.settings as settings
from django.utils.text import slugify 
# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

BOOLEAN = (
    (0,"Draft"),
    (1,"Publish")
)


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
    description = models.TextField(max_length=500,default='Type content here...')
    created_on = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='category', null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/challenges_images")
    org_tag = models.ForeignKey("organisations.Organisation", on_delete=models.SET_NULL, related_name='challengeorgtag', null=True)

    def __str__(self):
        return self.title


class Idea(models.Model):
    
    title = models.CharField(max_length=200, unique=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ideas', null=True)
    slug = models.SlugField(max_length=200, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='idea_author', null=True)
    estimated_cost = models.DecimalField(max_digits=6, decimal_places=2, default=300)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500,default='Type content here...')
    notes = models.TextField(max_length=500,default='Type content here...', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_user_led = models.BooleanField(default=True)
    is_similar = models.BooleanField(default=False, null=True)
    is_approved = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/idea_images")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_department', null=True, blank=True)
    sub_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='idea_sub_department', null=True)
    likes = models.ManyToManyField(Account, related_name='idea_likes')
    STAGES = [
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('in development', 'In development'),
    ('complete', 'Complete'),
]
    stage = models.CharField(max_length=2000, choices=STAGES, blank=True, null=True)
    org_tag = models.ForeignKey("organisations.Organisation", on_delete=models.SET_NULL, related_name='ideaorgtag', null=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_winner(self, challenge):
        print(self.likes.count(max))
        return self.likes.count(max)

    # def __str__(self):
    #     return "£ " + str(self.estimated_cost)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Idea, self).save(*args, **kwargs)


class IdeaComment(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='idea_comment_author', null=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500,default='Type content here...')
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='idea_comment_likes', blank=True)
    image = models.ImageField(upload_to='images/', default='images/gender.png', null=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments', default=0)
        
    class Meta:
        ordering = ['-created_on']
  

