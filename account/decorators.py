from django.contrib.auth import decorators
from django.http import HttpResponse
from django.shortcuts import redirect, render
# from django import template
# from django.contrib.auth.models import Group 

# register = template.Library() 

# @register.filter(name='is_group') 
# def is_group(user, group_name):
#     group =  Group.objects.get(name=group_name) 
#     return group in user.groups.all() 


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            
            # return redirect('public_landing')

            return redirect('blogfeed_main')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('Working:', allowed_roles)

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
