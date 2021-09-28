from django.contrib.auth import decorators
from django.http import HttpResponse
from django.shortcuts import redirect, render
from organisations.models import Organisation
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import logging

# register = template.Library() 

# @register.filter(name='is_group') 
# def is_group(user, group_name):
#     group =  Group.objects.get(name=group_name) 
#     return group in user.groups.all() 


def unauthenticated_user(view_func):
    # orgslug = Organisation.objects.get(slug=orgslug)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            logging.error('Working:', allowed_roles)

            group = None 
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'errors/access_denied.html')
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def admin_only(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None 
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'admins':
                return view_func(request, *args, **kwargs)
            else:
                return redirect("public_landing")
        return wrapper_func

def has_org_access(allowed_orgs=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            logging.error('Working:', allowed_orgs)
            org_tag = None 
            if request.user.org_tag.exists():
                org_tag = request.user.org_tag
            if org_tag in allowed_orgs:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'errors/access_denied.html')
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

# def has_org_access(user): 
#     return True if user.affilated_with is True else False

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='enter'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_affiliated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator