from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from account.models import Account
from django.contrib.auth.models import PermissionsMixin
from . import models
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
    site_header = 'User Database'

class TestAdminPermissions(admin.ModelAdmin):
    site_header = 'User Database'

user_site = UserAdminArea(name='BlogAdmin')

user_site.register(models.Account)