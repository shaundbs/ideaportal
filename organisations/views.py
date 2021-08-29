from django.shortcuts import render
from .models import Organisation
from django.views import generic

# Create your views here.
def select_org(request):
    orgs = Organisation.objects.all()
    context={
      'orgs':orgs
    }


    return  render(request, 'organisations/orghub.html', context)