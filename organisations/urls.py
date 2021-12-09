from django.urls import path
from . import views

urlpatterns = [
    path('select-an-organisation/<int:pk>', views.select_org, name='select_org'),
]