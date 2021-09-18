from django import template
from django.contrib.auth.models import Group 
from account.models import Account

register = template.Library() 

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name='has_access')
def has_org_access(user): 
    return True if user.affilated_with is True else False

