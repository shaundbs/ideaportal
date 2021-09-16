from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from account.models import Account
from django.contrib.auth.models import PermissionsMixin
from . import models
from blog.models import Comment, Post
from organisations.models import Organisation
from challenges.models import Department, Challenge, IdeaComment, Idea
# Register your models here.


class AccountAdmin(UserAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    model = Account
    list_display = ('email', 'username', 'age', 'date_joined', 'last_login', 'is_admin', 'is_staff','is_email_verified', 'group')
    search_fields = ('email', 'username')
    # groups 
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)

class UserAdminArea(admin.AdminSite):
    site_header = 'Idea Portal Management'

class UserAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True
        return False

class PostAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True
        return False

class CommentAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True
        return False


class OrganisationAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True
        return False

class DepartmentAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['portal_managers', 'admins']).exists():
            return True
        return False

class CommentAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True
        return False

class IdeaCommentAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True
        return False

class ChallengeAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True
        return False

class IdeaAdminPermissions(admin.ModelAdmin):
    def has_add_permission(self, request):

        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_change_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_delete_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True

        return False

    def has_view_permission(self, request, obj = None):
        if request.user.groups.filter(name__in=['challenge_managers', 'admins']).exists():
            return True
        return False

user_site = UserAdminArea(name='BlogAdmin')

user_site.register(models.Account, UserAdminPermissions)
user_site.register(Post, PostAdminPermissions)
user_site.register(Comment, CommentAdminPermissions)
user_site.register(Organisation, OrganisationAdminPermissions)
user_site.register(Department, DepartmentAdminPermissions)
user_site.register(IdeaComment, IdeaCommentAdminPermissions)
user_site.register(Challenge, ChallengeAdminPermissions)
user_site.register(Idea, IdeaAdminPermissions)