from django.urls import path
from . import views

urlpatterns = [
    path('select-an-organisation/', views.select_org, name='select_org'),
]