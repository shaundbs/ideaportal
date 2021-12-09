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
from account.admin import user_site
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

"""
Issue: add '/' to the end of each pattern
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ideaportal-management/', user_site.urls),
<<<<<<< HEAD
    path('home', views.home, name='home'),
=======
    path('home/', views.home, name='home'),
>>>>>>> idea-solo
    path('info/admin-info', views.admin_info, name='admin_info'),
    path('info/portal-manager-info', views.portal_manager_info, name='portal_manager_info'),
    path('info/challenge-manager-info', views.challenge_manager_info, name='challenge_manager_info'),
    path('info/nhs-staff-info', views.nhs_staff_info, name='nhs_staff_info'),
    path('info/public-info', views.public_info, name='public_info'),

    path('', views.enter, name='enter'),
    path('logout', views.logoutUser, name='logout'),
    path('index', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='emails/password_reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='emails/password_reset_confirm.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='emails/password_reset_done.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='emails/password_reset_complete.html'), name='password_reset_complete' ),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('auth/create-an-account/<slug:slug>', views.auth_username, name='auth_username'),
    path('auth/enter-your-nhs-number/', views.auth_number, name='auth_number'),
    path('auth/enter-your-date-of-birth/', views.auth_age, name='auth_age'),
    path('<slug:slug>/edit-age/', views.edit_age, name='edit_age'),
    path('<slug:slug>/edit-email/', views.edit_email, name='edit_email'),
    path('<slug:slug>/edit-profile-image/', views.edit_profile, name='edit_profile_image'),


    path('auth/are-you-an-employee?/', views.auth_employee, name='auth_employee'),
    path('auth/choose-your-interests/', views.choose_interests, name='choose_interests'),
    path('auth/registration-success/', views.success, name='registration_success'),
    path('auth/account-activation-success/', views.activation_success, name='activation_success'),

    path('landing/public/', views.public_landing, name='public_landing'),
    path('blogs/post-feed/<slug:slug>/', views.blogfeed_main.as_view(), name='blogfeed_main'),
    path('blogs/post-feed/<slug:slug>/edit', views.blogfeed_main_edit.as_view(), name='blogfeed_main_edit'),

    path('blogs/post-feed/challenges/', include('blog.urls'), name='feed'),
    path('challenges/', include('challenges.urls'), name='challengehub'),
    path('organisations/', include('organisations.urls'), name='organisations'),
    path('orchaapi/', include('orchaapi.urls'), name='apihub'),
    path('ideastore/', include('ideastore.urls'), name='ideastore'),

    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('<slug:slug>/profile/profile-main', views.profile_main, name='profile_main'),
    path('auth/testform/', views.testing, name='testing'),

    path('/blogs/post-feed/', views.index),

    # FOR BETA ONLY
    path('<slug:slug>/feedback/', views.feedback, name='feedback'),
    path('<slug:slug>/feedback-successful/', views.feedback_successful, name='feedback_successful'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
