"""ideaportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import re_path
import account.views as views
import challenges.views as cviews
import blog.views as bviews
from django.urls import path, include
import blog.urls
from account.forms import CustomUserCreationForm, AgeForm, EmployeeForm
from django.conf.urls.static import static
import ideaportal.settings
from django.conf import settings
from orchaapi.views import GetDroplets
from django.conf import settings
from django.contrib.auth import views as auth_views

named_contact_forms = (
    ('contactdata', CustomUserCreationForm),
    ('agedata', AgeForm),
    ('employeedata', EmployeeForm),
)

contact_wizard = views.ContactWizard.as_view(named_contact_forms,
    url_name='contact_step', done_step_name='finished')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('', views.enter, name='enter'),
    path('logout', views.logoutUser, name='logout'),
    path('index', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='emails/password_reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='emails/password_reset_confirm.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='emails/password_reset_done.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='emails/password_reset_complete.html'), name='password_reset_complete' ),


    path('auth/create-an-account/', views.auth_username, name='auth_username'),
    path('auth/enter-your-nhs-number/', views.auth_number, name='auth_number'),
    path('auth/enter-your-date-of-birth/', views.auth_age, name='auth_age'),
    path('auth/are-you-an-employee?/', views.auth_employee, name='auth_employee'),
    path('auth/choose-your-interests/', views.choose_interests, name='choose_interests'),
    path('auth/registration-success/', views.success, name='registration_success'),
    path('auth/account-activation-success/', views.activation_success, name='activation_success'),

    path('landing/public/', views.public_landing, name='public_landing'),
    path('blogs/post-feed/<slug:slug>/', views.blogfeed_main.as_view(), name='blogfeed_main'),
    path('blogs/post-feed/<slug:slug>/edit', views.blogfeed_main_edit.as_view(), name='blogfeed_main_edit'),

    # path('challenges/<slug:slug>/', bviews.PostDetail.as_view, name='post_detail'),
    path('blogs/post-feed/challenges/', include('blog.urls'), name='feed'),
    # path('blogs/post-feed/challenges/likes/', include('blog.urls'), name='likes'),
    path('challenges/', include('challenges.urls'), name='challengehub'),
    path('organisations/', include('organisations.urls'), name='organisations'),

    path('orchaapi/', include('orchaapi.urls'), name='apihub'),


    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('profile/profile-main', views.profile_main, name='profile_main'),
    path('auth/testform/', views.testing, name='testing'),
    path('auth/raindrops', GetDroplets.as_view(template_name='core/droplets.html'), name='Droplet View'),


    # re_path(r'^contact/(?P<step>.+)/$', contact_wizard, name='contact_step'),
    # path('contact/', contact_wizard, name='contact'),

    # path('auth/create-an-account/', views.ContactWizard.as_view([account.forms.CustomUserCreationForm,account.forms.AgeForm, account.forms.EmployeeForm]), name='contact'),

#       path('auth/create-an-account', views.ContactWizard.as_view(views.FORMS, condition_dict={'contact':'contact',
#     'age':'age', 'employee':'employee' }), name='contact')
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
