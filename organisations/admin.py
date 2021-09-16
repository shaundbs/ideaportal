from django.contrib import admin
from .models import Organisation

# Register your models here.
class OrgAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','specialty', 'description', 'created_on')
    list_filter = ("specialty",)
    search_fields = ['name', 'specialty']

    filter_horizontal = ()
    fieldsets = ()

class OrgAdmin(admin.ModelAdmin):
    list_display = ('name','is_active','specialty', 'description', 'created_on')
    list_filter = ("specialty",)
    search_fields = ['name', 'specialty']

    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Organisation, OrgAdmin)

