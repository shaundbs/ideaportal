from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.views.generic import TemplateView
import requests, json

class GetDroplets(TemplateView):
    template_name = 'core/droplets.html'
    def get_context_data(self, *args, **kwargs):
        pass
