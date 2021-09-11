from operator import mod
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import NullBooleanField
from account.models import Account
from django.utils.text import slugify 
from django.db.models import Count
# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, null=True, default='none')
    SEVERITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]
    severity = models.CharField(max_length=32, choices=SEVERITY_CHOICES, default='low')
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='blog_posts', null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    department = models.ForeignKey('challenges.Department', on_delete=SET_NULL, related_name='dept', null=True)
    likes = models.ManyToManyField(Account, related_name='post_likes', null=True, blank=True)
    challenge = models.ForeignKey('challenges.Challenge', related_name='post_to_challenge', on_delete=CASCADE, null=True)
    startDate = models.DateField(null=True, blank=True)
    endDate =  models.DateField(null=True, blank=True)
    description = models.TextField(max_length=500,default='Type content here...')
    manager = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='challenge_manager', null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    winner = models.ForeignKey('challenges.Idea', on_delete=models.SET_NULL, related_name='winner', null=True, blank=True)
    org_tag = models.ForeignKey('organisations.Organisation', on_delete=models.SET_NULL, related_name='postorgtag', null=True)

    # winning_idea = models.OneToOneField('challenges.Idea', on_delete=models.SET_NULL, related_name='winning_idea', null=True, blank=True)
    #  winning_idea = all_ideas.order_by("likes")[:1]
    #         winning_idea_id = winning_idea.values('id')[0]['id']
    #         winning_idea_slug = winning_idea.values('slug')[0]['slug']
    #         print(winning_idea_slug)
    #         context['winnerpk'] = winning_idea_id
    #         context['winnerslug'] = winning_idea_slug

    def total_likes(self):
        return self.likes.count()

    def total_likes_received(user):
        return user.posts.aggregate(total_likes=Count('likes'))['total_likes'] or 0

    # def get_winner(post, pk):
    #     range = post.winner.filter(post=pk)
    #     chosen = range.order_by('likes')[:1]
    #     return chosen

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.winner = self.winner.likes.count(max)
        super(Post, self).save(*args, **kwargs)

    def create_post(self, author, title, severity, department, challenge, description):
        if not title:
            raise ValueError("Title is a required field")
        if not description:
            raise ValueError("Description is a required field")
        post = self.model(
            author = author,
            severity=severity,
            department=department,
            challenge=challenge,
            description=description
        )
        post.save(using=self._db)
        return post


class Comment(models.Model):
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='comment_author', null=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=500,default='Type content here...')
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name='comment_likes')
    image = models.ImageField(upload_to='images/', default='images/gender.png', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=0)

    # def __str__(self):
    #     return '%s - %s' % (self.post.title, self.post.content)

    class Meta:
        ordering = ['-created_on']

