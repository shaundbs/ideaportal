import logging
import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.utils.timezone import make_aware
from django.urls import reverse

from challenges.models import Post, Idea, OrgForm
from organisations.models import Organisation


"""Below are the calsses for views of [Management] tab 

Classes:
- ListView:
    PostList: [Pending Challenges]
    PostListCompleted: [Completed Challenges]
    PendingIdeasList: [Pending Ideas]
- DetailView:
    PostManagementDetail: [Pending Challenges]
    IdeaManagementDetail: [Manage Pending Idea]

Function:
- approve_idea
- reject_idea
"""

class PostList(ListView):
    """View for Pending Challenges under Management tab"""
    today = make_aware(datetime.datetime.now())
    template_name = 'error/access_denied.html'
    manage_template_name = 'management/manager_index.html'
    model = Post
    paginate_by = 4

    def setup(self, request, *args, **kwargs):
        if request.user.is_admin:
            self.template_name = self.manage_template_name
        return super().setup(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(status=0).filter(org_tag=portal_choice).filter(endDate=None).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        context['orgslug'] = portal_slug            
        return context

class PostListCompleted(PostList):
    """View for Completed Challenges under Management tab"""
    manage_template_name = 'management/completed_challenges.html'

    def get_queryset(self, *args, **kwargs):
        today = make_aware(datetime.datetime.now())
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(status=1).filter(org_tag=portal_choice).filter(endDate__lte=today).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        return context

class PendingIdeasList(PostList):
    manage_template_name = 'management/pending_ideas.html'
    context_object_name = 'ideas'
    model = Idea

    def get_queryset(self, *args, **kwargs):
        portal_choice = self.kwargs['slug']
        logging.error(portal_choice)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(status=0).filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ApprovedIdeaList(PostList):
    manage_template_name = 'management/pending_ideas.html'
    context_object_name = 'ideas'
    model = Idea

    def get_queryset(self, *args, **kwargs):
        portal_choice = self.kwargs['slug']
        logging.error(portal_choice)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(status=0).filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostManagementDetail(DetailView):

    model = Post
    template_name = "management/post_management_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostManagementDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        active = False

        if stuff.endDate == None:
            active = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["is_active"] = active

        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug
        context["orgslug"] = portal_slug
        return context

class IdeaManagementDetail(DetailView):
    
    model = Idea
    template_name = 'management/idea_management_detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(IdeaManagementDetail, self).get_context_data()
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        context['orgslug'] = portal_slug
        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        idea_pridar = stuff.is_pridar
        custom = False
        if idea_pridar:
            customised = OrgForm.objects.get(title = stuff.title)
            custom = True
            context['in_sandbox'] = customised.in_sandbox
            context['is_released_and_supported'] = customised.is_released_and_supported
            context['is_open_source_partnership'] = customised.is_open_source_partnership
            context['NICE_Tier1_DTAC_evidence_in_place'] = customised.NICE_Tier1_DTAC_evidence_in_place
            context['NICE_Tier2_DTAC_evidence_in_place'] = customised.NICE_Tier2_DTAC_evidence_in_place
            context['risk_and_mitigations_are_public'] = customised.risk_and_mitigations_are_public
            context['ce_mark_dcb_register'] = customised.ce_mark_dcb_register
            context['safety_officer_stated'] = customised.safety_officer_stated
            context['iso_supplier'] = customised.iso_supplier
            context['user_kpis_is_an_ai_pathway_are_defined'] = customised.user_kpis_is_an_ai_pathway_are_defined
            context['user_to_board_approval_obtained'] = customised.user_to_board_approval_obtained
            context['cost_of_dev_and_support_agreed'] = customised.cost_of_dev_and_support_agreed
            context['ip_agreement_in_place'] = customised.ip_agreement_in_place
            context['ig_agreements_in_place'] = customised.ig_agreements_in_place
            context['data_and_model_agreed'] = customised.data_and_model_agreed
        context['custom'] = custom
        return context

def approve_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    logging.error(idea.status)
    idea.status = 1
    idea.stage = 'open'
    idea.save()

    return HttpResponseRedirect(reverse('pending_ideas', args=[orgslug]))

def reject_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    logging.error(idea.status)
    idea.status = 1
    idea.stage = 'rejected'
    idea.save()

    return HttpResponseRedirect(reverse('pending_ideas', args=[orgslug]))