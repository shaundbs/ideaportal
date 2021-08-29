from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.views.generic import TemplateView
import requests, json

# def home(request):
#     response = requests.post('https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate')
#     geodata = response.json()
#     return render(request, 'core/home.html', {
#         'ip': geodata['ip'],
#         'country': geodata['country_name']
#     })


class GetDroplets(TemplateView):
    template_name = 'core/droplets.html'
    def get_context_data(self, *args, **kwargs):
        pass

# data = { 'username' : 'cnwl', 'password' : 'K2Q5!ZqnJ!#RYV'}
# r = requests.post('https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate', data=json.dumps(data), verify=False)
# token = json.loads(r.text)['session']
# print(token)