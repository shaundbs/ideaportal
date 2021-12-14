from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'slug', 'status','created_on', 'severity', 'challenge', 'department', 'startDate', 'endDate',)
    list_filter = ("status",)
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

    filter_horizontal = ()
    fieldsets = ()

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'updated_on', 'comment','created_on')
    list_filter = ("author",)
    search_fields = ['author', 'comment', 'likes']

    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)