from django.contrib import admin
from .models import Challenge, Idea, Department, IdeaComment

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title','description','image', 'severity','author', 'department')
    list_filter = ("severity",)
    search_fields = ['title', 'description']
    # prepopulated_fields = {'slug': ('title',)}

    # readonly_fields = ('id')

    filter_horizontal = ()
    fieldsets = ()

class IdeasAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'status', 'estimated_cost', 'post', 'is_user_led','is_similar','is_approved', 'author', 'department', 'image', 'created_on', 'stage', )
    list_filter = ("status",)
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

    # readonly_fields = ('id')

    filter_horizontal = ()
    fieldsets = ()

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','department','sub_department', 'is_approved', 'is_core')
    list_filter = ("department", 'is_approved', 'is_core')
    search_fields = ['department', 'sub_department', 'is_approved', 'is_core']

    filter_horizontal = ()
    fieldsets = ()

class IdeaCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'updated_on', 'comment','created_on')
    list_filter = ("author",)
    search_fields = ['author', 'comment', 'likes']

    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Idea, IdeasAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(IdeaComment, IdeaCommentAdmin)