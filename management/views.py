import logging
import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.utils.timezone import make_aware
from django.urls import reverse
from account.views import access_denied

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

class ManagementListView(ListView):
    """Abstract class for the ListView classes in [Management]"""
    today = make_aware(datetime.datetime.now())
    template_name = None
    model = None
    paginate_by = 4

    def setup(self, request, *args, **kwargs):
        """Override the setup method, redirect to [Access Denied] if user is not admin"""
        if not request.user.is_admin:
            orgslug = Organisation.objects.get(slug=self.kwargs['slug']).slug
            return HttpResponseRedirect(reverse('ideaportal:access_denied'), args=[orgslug])
        return super().setup(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = Organisation.objects.get(slug=self.kwargs['slug'])         
        return context

class PostList(ManagementListView):
    """View for Pending Challenges under Management tab"""
    template_name = 'management/manager_index.html'
    model = Post

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        return query_set.filter(status=0).filter(endDate=None).order_by('-created_on')

class PostListCompleted(ManagementListView):
    """View for Completed Challenges under Management tab"""
    template_name = 'management/completed_challenges.html'
    model = Post

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        return query_set.filter(status=1).filter(endDate__lte=self.today).order_by('-created_on')


class PendingIdeasList(ManagementListView):
    template_name = 'management/pending_ideas.html'
    model = Idea
    context_object_name = 'ideas'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        return query_set.filter(status=0)

class ApprovedIdeaList(ManagementListView):
    template_name = 'management/pending_ideas.html'
    model = Idea
    context_object_name = 'ideas'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        return query_set.filter(status=1)


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
        context['org'] = portal_choice
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
        context['org'] = Organisation.objects.get(slug=self.kwargs['orgslug'])
        return context

def change_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=pk)
    logging.error(idea.status)
    idea.status = 1
    idea.stage = request.POST.get('idea_id')
    idea.save()

    return HttpResponseRedirect(reverse('pending_ideas', args=[orgslug]))

def reject_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    logging.error(idea.status)
    idea.status = 1
    idea.stage = 'rejected'
    idea.save()

    return HttpResponseRedirect(reverse('pending_ideas', args=[orgslug]))