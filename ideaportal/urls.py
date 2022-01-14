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

"""
Issue: add '/' to the end of each pattern
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ideaportal-management/', user_site.urls),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='emails/password_reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='emails/password_reset_confirm.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='emails/password_reset_done.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='emails/password_reset_complete.html'), name='password_reset_complete' ),

    path('', include('account.urls'), name='account'),
    path('blogs/post-feed/challenges/', include('blog.urls'), name='feed'),
    path('challenges/', include('challenges.urls'), name='challengehub'),
    path('organisations/', include('organisations.urls'), name='organisations'),
    path('orchaapi/', include('orchaapi.urls'), name='apihub'),
    path('ideastore/', include('ideastore.urls'), name='ideastore'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
