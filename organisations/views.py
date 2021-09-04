from django.shortcuts import render
from .models import Organisation
from django.views import generic

# Create your views here.
def select_org(request):
    orgs = Organisation.objects.filter(is_active=True)
    # print(Organisation.objects.get(name='CNWL'))
    # pic = Organisation.get_profile_pic_url(Organisation.objects.get(name='CNWL'))
    # print(pic)
    # urls = orgs.image
    # print(urls)
    context={
      'orgs':orgs,
    }

    

    return  render(request, 'organisations/orghub.html', context)