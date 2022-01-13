from django.contrib import admin
from .models import Organisation

# Register your models here.
class OrgAdmin(admin.ModelAdmin):
    list_display = ('name','is_active', 'description', 'created_on')
    search_fields = ['name']

    filter_horizontal = ()
    fieldsets = ()

class OrgAdmin(admin.ModelAdmin):
    list_display = ('name','is_active', 'description', 'created_on')
    search_fields = ['name']

    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Organisation, OrgAdmin)

