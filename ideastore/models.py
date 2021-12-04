from django.db import models

from challenges.models import Idea

# Create your models here.
# class Post(models.Model):
#     """The model of the list of the challenges"""
#     title = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, null=True, default='none')
#     author = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='blog_posts', null=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)
#     department = models.ForeignKey('challenges.Department', on_delete=CASCADE, related_name='dept', null=True)
#     likes = models.ManyToManyField(Account, related_name='post_likes', null=True, blank=True)
#     idea = models.ForeignKey('challenges.Challenge', related_name='post_to_challenge', on_delete=CASCADE, null=True)
#     startDate = models.DateField(null=True, blank=True)
#     endDate =  models.DateField(null=True, blank=True)
#     description = models.TextField(max_length=500,default='Type content here...')
#     manager = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='challenge_manager', null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)
#     winner = models.ForeignKey('challenges.Idea', on_delete=models.SET_NULL, related_name='winner', null=True, blank=True)
#     org_tag = models.ForeignKey('organisations.Organisation', on_delete=models.SET_NULL, related_name='postorgtag', null=True)

#     def total_likes(self):
#         return self.likes.count()

#     def total_likes_received(user):
#         return user.posts.aggregate(total_likes=Count('likes'))['total_likes'] or 0


#     def total_likes_received(user):
#         return user.idea_author.aggregate(total_likes=Count('likes'))['total_likes'] or 0


#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         super(Post, self).save(*args, **kwargs)

#     def create_post(self, author, title, severity, department, challenge, description):
#         if not title:
#             raise ValueError("Title is a required field")
#         if not description:
#             raise ValueError("Description is a required field")
#         post = self.model(
#             author = author,
#             severity=severity,
#             department=department,
#             challenge=challenge,
#             description=description
#         )
#         post.save(using=self._db)
#         return post