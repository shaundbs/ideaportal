from . import views

from django.urls import path
from django.contrib.auth import views as auth_views

"""
Issue: add '/' to the end of each pattern
"""


urlpatterns = [
    path('home/', views.home, name='home'),
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

    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('<slug:slug>/profile/profile-main', views.profile_main, name='profile_main'),
    path('auth/testform/', views.testing, name='testing'),

    path('/blogs/post-feed/', views.index),

    # FOR BETA ONLY
    path('<slug:slug>/feedback/', views.feedback, name='feedback'),
    path('<slug:slug>/feedback-successful/', views.feedback_successful, name='feedback_successful'),
]