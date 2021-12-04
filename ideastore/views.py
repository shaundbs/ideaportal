from django.shortcuts import render
from django.views import generic
from django.core.paginator import *

from organisations.models import Organisation
from challenges.models import Idea

# Create your views here.

def view_ideas():
    pass

def submit_idea():
    pass

class IdeaList(generic.ListView):
    model = Idea
    paginate_by = 4
    template_name = 'ideastore/idea_list.html'
    context_object_name = 'ideas'

    def get_queryset(self, *args, **kwargs):
        """Issue: What kind of idea should be listed in the page, see status in
            challenges/model/Idea, including    
            ('open', 'Open'),
            ('under review', 'Under Review'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('in development', 'In development'),
            ('delivered', 'Delivered'),
        """
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Idea.objects.filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        list_ideas = Idea.objects.all()
        paginator = Paginator(list_ideas, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        context['org'] = Organisation.objects.get(slug=portal_slug)

        spec_on = False
        custom_form_on = portal_choice.custom_form_on
        if custom_form_on:
            spec_on = True

        context['spec_on'] = spec_on

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaStoreOrgSpecific(generic.ListView):
    pass

class IdeaStoreHealth(generic.ListView):
    pass

class IdeaStoreCulture(generic.ListView):
    pass

class IdeaStoreJobSatifiction(generic.ListView):
    pass

class IdeaStoreRelationship(generic.ListView):
    pass

class IdeaStoreLeadership(generic.ListView):
    pass

class IdeaStoreData(generic.ListView):
    pass

class IdeaStoreSearchBlog(generic.ListView):
    pass

class IdeaStoreMonth(generic.ListView):
    pass


