from django.core.exceptions import ValidationError
from django.shortcuts import render
from requests.adapters import Response
from .forms import IdeaForm, CriteriaForm, ChallengeForm, DepartmentForm, OrgSpecificForm, PRIDARForm
from django.shortcuts import redirect
from operator import pos
from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Challenge, Post, Idea, Department, OrgForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
import datetime
from django.utils.timezone import make_aware
from organisations.models import Organisation
from django.core.paginator import *
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets
from .serializers import IdeaSerializer
import requests, json
import logging
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.


class PostList(generic.ListView):
    """The view for managing the challenges"""

    today = make_aware(datetime.datetime.now())
    template_name = "blogs/manager_index.html"

    model = Post

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        return Post.objects.filter(status=0).filter(org_tag=portal_choice).filter(endDate=None).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)
        context["orgslug"] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


def approve_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get("idea_id"))
    logging.error(idea.status)
    idea.status = 1
    idea.stage = "open"
    logging.error(idea.status)
    idea.save()

    return HttpResponseRedirect(reverse("idea_management_detail", args=[orgslug, str(pk), slug]))


def reject_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get("idea_id"))
    logging.error(idea.status)
    idea.status = 0
    logging.error(idea.status)
    idea.save()

    return HttpResponseRedirect(reverse("idea_management_detail", args=[orgslug, str(pk), slug]))


# IdeaApprovalForm


class PendingIdeasList(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = "ideas/pending_ideas.html"
    context_object_name = "ideas"
    # queryset = Idea.objects.all()

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = self.kwargs["slug"]
        logging.error(portal_choice)
        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        return Idea.objects.filter(status=0).filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super(PendingIdeasList, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)
        context["orgslug"] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class Statistics(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = "stats/stats.html"

    model = Organisation
    queryset = Organisation.objects.all()
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(Statistics, self).get_context_data(**kwargs)
        list_challenges = Organisation.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        context["slug"] = self.kwargs["slug"]

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)
        context["orgslug"] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaManagementDetail(generic.DetailView):

    model = Idea
    template_name = "ideas/idea_management_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaManagementDetail, self).get_context_data()
        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug
        context["orgslug"] = portal_slug
        stuff = get_object_or_404(Idea, id=self.kwargs["pk"])
        logging.error(stuff.is_pridar)
        idea_pridar = stuff.is_pridar
        logging.error(idea_pridar)
        custom = False
        if idea_pridar:
            customised = OrgForm.objects.get(title=stuff.title)
            custom = True
            context["in_sandbox"] = customised.in_sandbox
            context["is_released_and_supported"] = customised.is_released_and_supported
            context["is_open_source_partnership"] = customised.is_open_source_partnership
            context["NICE_Tier1_DTAC_evidence_in_place"] = customised.NICE_Tier1_DTAC_evidence_in_place
            context["NICE_Tier2_DTAC_evidence_in_place"] = customised.NICE_Tier2_DTAC_evidence_in_place
            context["risk_and_mitigations_are_public"] = customised.risk_and_mitigations_are_public
            context["ce_mark_dcb_register"] = customised.ce_mark_dcb_register
            context["safety_officer_stated"] = customised.safety_officer_stated
            context["iso_supplier"] = customised.iso_supplier
            context["user_kpis_is_an_ai_pathway_are_defined"] = customised.user_kpis_is_an_ai_pathway_are_defined
            context["user_to_board_approval_obtained"] = customised.user_to_board_approval_obtained
            context["cost_of_dev_and_support_agreed"] = customised.cost_of_dev_and_support_agreed
            context["ip_agreement_in_place"] = customised.ip_agreement_in_place
            context["ig_agreements_in_place"] = customised.ig_agreements_in_place
            context["data_and_model_agreed"] = customised.data_and_model_agreed
        context["custom"] = custom

        return context


class PostListCompleted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)
    queryset = Post.objects.filter(status=1).filter(endDate__lte=today)
    template_name = "blogs/completed_challenges.html"

    model = Post

    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(PostListCompleted, self).get_context_data(**kwargs)
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)
        context["orgslug"] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListOpen(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)
    template_name = "ideas/index_open.html"

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs["pk"])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage="open").filter(org_tag=portal_id).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(IdeaListOpen, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        logging.error(self.kwargs["pk"])
        context["orgslug"] = self.kwargs["slug"]
        context["title"] = "Open Ideas"
        context["pk"] = self.kwargs["pk"]
        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListDelivered(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)

    template_name = "ideas/index_open.html"

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs["pk"])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage="delivered").filter(org_tag=portal_id).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(IdeaListDelivered, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        logging.error(self.kwargs["pk"])
        context["title"] = "Delivered Ideas"
        context["slug"] = self.kwargs["slug"]
        context["pk"] = self.kwargs["pk"]

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListReview(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)

    queryset = Idea.objects.filter(stage="under review")
    template_name = "ideas/index_open.html"

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs["pk"])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage="under review").filter(org_tag=portal_id).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(IdeaListReview, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        logging.error(self.kwargs["pk"])
        context["slug"] = self.kwargs["slug"]
        context["title"] = "Under-review Ideas"
        context["pk"] = self.kwargs["pk"]

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListAccepted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)

    queryset = Idea.objects.filter(stage="accepted")
    template_name = "ideas/index_open.html"

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs["pk"])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage="accepted").filter(org_tag=portal_id).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(IdeaListAccepted, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        logging.error(self.kwargs["pk"])
        context["slug"] = self.kwargs["slug"]
        context["title"] = "Accepted Ideas"
        context["pk"] = self.kwargs["pk"]

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListInDev(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)

    queryset = Idea.objects.filter(stage="in development")
    template_name = "ideas/index_open.html"

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs["pk"])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage="in development").filter(org_tag=portal_id).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(IdeaListInDev, self).get_context_data(**kwargs)
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        context["slug"] = self.kwargs["slug"]
        logging.error(self.kwargs["pk"])
        context["title"] = "In-development Ideas"
        context["pk"] = self.kwargs["pk"]

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class History(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = "challenges/index_history.html"

    model = Organisation
    queryset = Organisation.objects.all()
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(History, self).get_context_data(**kwargs)
        list_challenges = Organisation.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        context["slug"] = self.kwargs["slug"]

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)
        context["orgslug"] = portal_slug
        context["current_org"] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class HistoryListCompleted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    logging.error(today)
    queryset = Post.objects.filter(status=1).filter(endDate__lte=today)
    template_name = "challenges/index_completed.html"

    model = Post

    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(HistoryListCompleted, self).get_context_data(**kwargs)
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


def submit_challenge_successful(request, slug):
    context = {"slug": slug}
    return render(request, "challenges/submit_challenge_success.html", context)


def submit_challenge(request, slug):
    """
    Called for both getting the challenge submission page and submitting a challenge

    Keyword Arguments:
    request -- the HTTP request that calls this.
    slug -- the url slug; identifies the organization that this challenge is being submitted in.

    Returns either the submit challenge page, or a redirect to the success page
    """
    # if the user is logged in, we can tag the request to the user (and should give an option to post anonymously anyway)
    if request.user.is_authenticated:
        # Generates a new form to store the challenge data
        form = ChallengeForm()
        logging.error(slug)
        org = slug
        orgobject = Organisation.objects.get(slug=slug)

        # If the type of request we're getting is a POST request then we're being given a completed form to send
        if request.method == "POST":
            form = ChallengeForm(request.POST, request.FILES)

            if form.is_valid():
                form.author = request.user
                challenge = form.save()
                challenge.org_tag = orgobject
                # If the challenge is NOT flagged to be anonymous, we need to get the user from the request
                if challenge.anonymous != True:
                    challenge.author = request.user
                cnwl = False
                # Save the challenge form again, because we've made changes
                challenge = form.save()
                Post.objects.create(
                    author=challenge.author,
                    title=challenge.title,
                    severity=challenge.severity,
                    department=challenge.department,
                    challenge=challenge,
                    description=challenge.description,
                    org_tag=challenge.org_tag,
                    image=challenge.image,
                )

                # Redirect the user to the success page
                return redirect("submit_challenge_successful", slug=slug)

        # Else if the type of request ISN'T POST, the request it to get the webpage, so we format the context and render the page
        context = {"challengeform": form, "org": org, "custom_on": orgobject.custom_form_on, "orgslug": slug, "logged_in": True}

        return render(request, "challenges/submit_challenge.html", context)
    # Else the user isn't logged in, so the challenge is anonymous by default
    else:
        # Generates a new form to store the challenge data
        form = ChallengeForm()
        logging.error(slug)
        org = slug
        orgobject = Organisation.objects.get(slug=slug)

        # If the type of request we're getting is a POST request then we're being given a completed form to send
        if request.method == "POST":
            form = ChallengeForm(request.POST, request.FILES)

            if form.is_valid():
                challenge = form.save()
                challenge.org_tag = orgobject
                cnwl = False
                # Save the challenge form again, because we've made changes
                challenge = form.save()
                Post.objects.create(
                    title=challenge.title,
                    severity=challenge.severity,
                    department=challenge.department,
                    challenge=challenge,
                    description=challenge.description,
                    org_tag=challenge.org_tag,
                    image=challenge.image,
                )

                # Redirect the user to the success page
                return redirect("submit_challenge_successful", slug=slug)

        # Else if the type of request ISN'T POST, the request it to get the webpage, so we format the context and render the page
        context = {"challengeform": form, "org": org, "custom_on": orgobject.custom_form_on, "orgslug": slug, "logged_in": False}

        return render(request, "challenges/submit_challenge.html", context)


def orcha_api(request):

    data = '{"username" : "cnwl", "password":"K2Q5!ZqnJ!#RYV"}'
    data_2 = (
        '{"searchTerm": "Back Pain","pageNumber": "1", "pageSize": "12", "costIds": [],"capabilityIds": [],"designedForIds": [],"countryIds": []}'
    )

    headers = {"Content-type": "application/json", "Accept": "application/json"}

    response = requests.post("https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate", data=data, headers=headers)
    body = json.loads(response.text)
    access_token = body["result"]["accessToken"]

    headers_2 = {"Authorization": "Bearer " + str(access_token)}
    headers_3 = {"Content-type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + str(access_token)}
    response_2 = requests.get("https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories", headers=headers_2)
    body_2 = json.loads(response_2.text)
    categories = body_2["result"]
    category_list = []
    for category in categories:
        category_list.append(category["subCategoryName"])
    logging.error(category_list)
    return render(request)


class ideaform(CreateView):
    model = Idea
    template_name = "ideas/submit_ideas_form.html"
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(ideaform, self).get_context_data(**kwargs)
        obj = get_object_or_404(Post, pk=self.kwargs["pk"])
        context["object"] = context["post"] = obj
        challenge_choice = Post.objects.get(slug=self.kwargs["slug"])
        challenge_slug = Post.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(challenge_slug)

        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug
        context["orgslug"] = portal_slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        custom_on = portal_choice.custom_form_on
        logging.error(custom_on)
        is_pridar = False
        if custom_on:
            is_pridar = True
        logged_in = False
        if self.request.user.is_authenticated:
            logged_in = True
        context["logged_in"] = logged_in
        context["challenge"] = Post.objects.get(slug=challenge_slug)
        context["custom_on"] = is_pridar

        context
        return context

    def form_valid(self, form):
        """Set field for form, then redirect to get_success_url"""
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        orgslug = self.kwargs["orgslug"]
        slug = self.kwargs["slug"]

        return reverse_lazy(
            "criteria",
            kwargs={
                "orgslug": orgslug,
                "pk": pk,
                "slug": slug,
            },
        )


def search_idea(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        ideas = Idea.objects.filter(title__icontains=searched, stage__isnull=False, description__icontains=searched)

        org_list = []
        org_tag_list = []
        for i in ideas:
            org_list.append(i)
            org_tag_list.append(i.org_tag)
            logging.error("Hellllo")
            logging.error(i.org_tag)

        zipped_values = zip(org_list, org_tag_list)

        return render(request, "search/selected_idea_search.html", {"searched": searched, "ideas": ideas, "zipped_values": zipped_values})
    else:
        return render(request, "search/selected_idea_search.html", {})


def idea_criteria_form(request, orgslug, pk, slug):
    """This function need to be refactor,
    1. This function is too long
    2. there is a almost same function in ideastore,
       with only different in the link of successful submission.
    """
    logging.error(pk)
    post = Post.objects.get(slug=slug)
    org = Organisation.objects.get(slug=orgslug)
    org_name = org.name
    activate_api = False
    api_on = org.api_on
    if api_on:
        activate_api = True
    logging.error(org.name)
    publish_publicly = False
    if org_name == "Public":
        publish_publicly = True
    # idea = Idea.objects.filter(author=request.user).latest('created_on')
    current_idea = Idea.objects.latest("created_on")
    logging.error(current_idea)
    logging.error(post.title)
    is_pridar = current_idea.is_pridar
    # is_pridar = org.custom_form_on
    logging.error(is_pridar)
    if is_pridar is True:
        form = PRIDARForm()
        if activate_api:
            # authentication credential for ORCHA API
            data = '{"username" : "cnwl", "password":"K2Q5!ZqnJ!#RYV"}'

            # header configuration to define format of data
            headers = {"Content-type": "application/json", "Accept": "application/json"}

            # authentication end point call to generate an access token to peform other REST API calls
            response = requests.post("https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate", data=data, headers=headers)
            # create a JSON from the string generated from the response
            body = json.loads(response.text)
            # parse the JSON to extract the access token and save as its own variable
            access_token = body["result"]["accessToken"]

            # configure another header that uses the access token from the authentication end point
            headers_2 = {"Authorization": "Bearer " + str(access_token)}
            headers_3 = {"Content-type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + str(access_token)}
            # sub-category endpoint call to extract all categories that ORCHA use to define its applications
            response_2 = requests.get(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories", headers=headers_2
            )
            # create a JSON from the string generated from the response
            body_2 = json.loads(response_2.text)
            # parse the JSON to extract the list of categories
            categories = body_2["result"]
            category_list = []
            # append the list of categories to a list format to make it easy to operate on
            for category in categories:
                category_list.append(category["subCategoryName"])

            # get user idea title
            compare = current_idea.title
            # get user idea title
            compare_desc = current_idea.description
            title_list = []
            description_list = []

            # append key words form title to list
            for word in compare.split():
                title_list.append(word)
            logging.info(title_list)

            for word in compare_desc.split():
                description_list.append(word)

            # initiate state variable
            is_similar = False
            category_names = []

            category_list_lower = [item.lower() for item in category_list]
            title_list_lower = [item.lower() for item in title_list]
            description_list_lower = [item.lower() for item in description_list]

            # if the keywords from the idea match any sub category areas set state to True and create a list of the similar terms
            existing_ideas = ""

            if (set(category_list_lower) & set(title_list_lower)) & set(description_list_lower):
                logging.info("This idea could be similar to an exisiting solution")
                is_similar = True
                logging.info("MATCH ALERT")
                category_names = list(set(category_list_lower) & set(title_list_lower) & set(description_list_lower))
                logging.info(category_names)
            else:
                logging.info("This idea is not similar to an exisitng solution")

            # append key words from title and description to list
            keywords = []
            keyterms = []
            for name in category_names:
                name.split()
                keywords.append(name)
            logging.info(keywords)

            # for each key word identified search in ORCHA for an application with the same keyword in title

            for category in keywords:
                data_2 = (
                    '{"searchTerm": "'
                    + category
                    + '","pageNumber": "1", "pageSize": "12", "costIds": [],"capabilityIds": [],"designedForIds": [],"countryIds": []}'
                )
                response_3 = requests.post(
                    "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Review/SearchPagedReviews", data=data_2, headers=headers_3
                )
                # create a JSON from the string generated from the response
                json_str = json.loads(response_3.text)
                # parse the JSON to extract the applications
                existing_ideas = json_str["result"]["items"]
                counter = 0
                # count the number of applications that the algorithm recorgnises as similar solutions
                for id in existing_ideas:
                    counter = counter + 1

                existing_idea_names = []
                existing_publisher_names = []
                existing_descriptions = []
                existing_links = []
                exisiting_platforms = []

                # for each application extract the name, download link, platform etc.
                for idea in existing_ideas:
                    existing_idea_names.append(idea["appName"])
                    existing_publisher_names.append(idea["publisherName"])
                    existing_descriptions.append(idea["description"])
                    existing_links.append(idea["downloadLink"])
                    exisiting_platforms.append(idea["platform"])

                zipped_values = zip(existing_idea_names, existing_publisher_names, existing_descriptions, existing_links, exisiting_platforms)
                logging.info(zipped_values)

        if request.method == "POST":
            form = PRIDARForm(request.POST)
            current_org = Organisation.objects.get(slug=orgslug)
            if form.is_valid():
                pridar_idea = form.save()
                pridar_idea = OrgForm.objects.latest("created_on")
                pridar_idea.title = current_idea.title
                pridar_idea.description = current_idea.description
                pridar_idea.image = current_idea.image
                if not current_idea.anonymous and current_idea.anonymous != None:
                    pridar_idea.author = request.user
                    current_idea.author = request.user
                pridar_idea.post = current_idea.post
                current_idea.org_tag.add(org)
                current_idea.department = post.department
                pridar_idea.org_tag.add(org)
                pridar_idea.department = post.department
                estimated_cost = form.cleaned_data.get("estimated_cost")
                notes = form.cleaned_data.get("notes")
                pridar_idea.notes = notes
                current_idea.notes = notes
                is_user_led = form.cleaned_data.get("is_user_led")
                is_public = form.cleaned_data.get("is_public")
                public = Organisation.objects.get(name="Public")
                pridar_idea.save()
                current_idea.save()

                return redirect("submit_success", orgslug=orgslug, pk=pk, slug=slug)

        try:
            context = {
                "criteriaform": form,
                "publish_publicly": publish_publicly,
                "existing_ideas": existing_ideas,
                "app_names": existing_idea_names,
                "publisher_names": existing_publisher_names,
                "app_descriptions": existing_descriptions,
                "download_links": existing_links,
                "app_platforms": exisiting_platforms,
                "zipped_values": zipped_values,
                "is_similar": is_similar,
                "counter": counter,
            }
        except:
            context = {"criteriaform": form, "publish_publicly": publish_publicly}

        return render(request, "ideas/idea_orgspecific_form.html", context)
    else:
        form = CriteriaForm()
        if activate_api:
            data = '{"username" : "cnwl", "password":"K2Q5!ZqnJ!#RYV"}'

            headers = {"Content-type": "application/json", "Accept": "application/json"}

            response = requests.post("https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate", data=data, headers=headers)
            body = json.loads(response.text)
            access_token = body["result"]["accessToken"]
            # logging.error(response.headers)
            # logging.error(access_token)

            headers_2 = {"Authorization": "Bearer " + str(access_token)}
            headers_3 = {"Content-type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + str(access_token)}
            # logging.error(headers_2)
            response_2 = requests.get(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories", headers=headers_2
            )
            # logging.error(response_2.text)
            body_2 = json.loads(response_2.text)
            categories = body_2["result"]
            category_list = []
            for category in categories:
                category_list.append(category["subCategoryName"])
            logging.error(category_list)
            logging.error(current_idea.description)

            # get idea title
            compare = current_idea.title
            compare_desc = current_idea.description
            title_list = []
            description_list = []

            # append key words form title to list
            for word in compare.split():
                title_list.append(word)
            logging.error(title_list)

            for word in compare_desc.split():
                description_list.append(word)

            # initiate state variable
            is_similar = False
            category_names = []

            category_list_lower = [item.lower() for item in category_list]
            title_list_lower = [item.lower() for item in title_list]
            description_list_lower = [item.lower() for item in description_list]

            # if the keywords from the idea match any sub category areas set state to True and create a list of the similar terms
            comparers = set(category_list_lower) & set(title_list_lower)
            logging.error(set(category_list_lower) & set(title_list_lower))
            ranger = set(category_list_lower) & set(title_list_lower)
            existing_ideas = ""

            if set(category_list_lower) & set(title_list_lower):
                logging.error("This idea could be similar to an exisiting solution")
                is_similar = True
                logging.error("MATCH ALERT")
                category_names = list(set(category_list_lower) & set(title_list_lower))
                logging.error(category_names)
            else:
                logging.error("This idea is not similar to an exisitng solution")

            # append key words form title to list
            keywords = []
            keyterms = []
            for name in category_names:
                name.split()
                keywords.append(name)
            logging.error(keywords)

            appName = ""
            clinicalAssuranceScore = ""
            userExperienceScore = ""
            publisherName = ""
            description = ""
            version = ""
            downloadLink = ""
            platform = ""

            for category in keywords:
                data_2 = (
                    '{"searchTerm": "'
                    + category
                    + '","pageNumber": "1", "pageSize": "12", "costIds": [],"capabilityIds": [],"designedForIds": [],"countryIds": []}'
                )
                response_3 = requests.post(
                    "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Review/SearchPagedReviews", data=data_2, headers=headers_3
                )
                json_str = json.loads(response_3.text)
                existing_ideas = json_str["result"]["items"]
                counter = 0
                for id in existing_ideas:
                    counter = counter + 1
                logging.error("Total isssssssss " + str(counter))

                # context_2 = {'existing_ideas': existing_ideas}
                existing_idea_names = []
                existing_publisher_names = []
                existing_descriptions = []
                existing_links = []
                exisiting_platforms = []

                for idea in existing_ideas:
                    existing_idea_names.append(idea["appName"])
                    existing_publisher_names.append(idea["publisherName"])
                    existing_descriptions.append(idea["description"])
                    existing_links.append(idea["downloadLink"])
                    exisiting_platforms.append(idea["platform"])

                zipped_values = zip(existing_idea_names, existing_publisher_names, existing_descriptions, existing_links, exisiting_platforms)
                logging.error(zipped_values)

        if request.method == "POST":
            form = CriteriaForm(request.POST)
            if form.is_valid():
                estimated_cost = form.cleaned_data.get("estimated_cost")
                logging.error(estimated_cost)
                current_idea.estimated_cost = estimated_cost
                notes = form.cleaned_data.get("notes")
                current_idea.notes = notes
                is_user_led = form.cleaned_data.get("is_user_led")
                is_public = form.cleaned_data.get("is_public")
                public = Organisation.objects.get(name="Public")
                if is_public:
                    current_idea.org_tag.add(public)
                current_idea.is_user_led = is_user_led
                if not current_idea.anonymous and current_idea.anonymous != None:
                    current_idea.author = request.user
                current_idea.org_tag.add(org)
                current_idea.department = post.department
                current_idea.save()

                return redirect("submit_success", orgslug=orgslug, pk=pk, slug=slug)

        try:
            context = {
                "criteriaform": form,
                "publish_publicly": publish_publicly,
                "existing_ideas": existing_ideas,
                "app_names": existing_idea_names,
                "publisher_names": existing_publisher_names,
                "app_descriptions": existing_descriptions,
                "download_links": existing_links,
                "app_platforms": exisiting_platforms,
                "zipped_values": zipped_values,
                "is_similar": is_similar,
                "counter": counter,
            }
        except:
            context = {"criteriaform": form, "publish_publicly": publish_publicly}

        return render(request, "ideas/idea_criteria_form.html", context)


def submit_success(request, orgslug, pk, slug):
    context = {"orgslug": orgslug}
    return render(request, "ideas/submit_success.html", context)


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all().filter(stage__isnull=False).order_by("title")
    serializer_class = IdeaSerializer


class CNWLIdeaViewSet(viewsets.ModelViewSet):
    cnwl_id = Organisation.objects.get(name="CNWL").id
    queryset = Idea.objects.filter(org_tag=cnwl_id).filter(stage__isnull=False).order_by("title")
    serializer_class = IdeaSerializer


def lifecycle(request, pk, slug):
    org = Organisation.objects.get(id=pk)
    org_slug = org.slug
    context = {"pk": pk, "orgslug": org_slug, "slug": slug}
    return render(request, "challenges/lifecycle.html", context)


class CommentList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blogs/index.html"


class PostDetail(generic.DetailView):
    model = Post
    template_name = "blogs/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked

        return context


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def intranet_api(request, stage=None):
    org = Organisation.objects.get(name="Public")
    org_slug = org.slug
    pk = org.id

    query_set = Idea.objects.filter(org_tag=pk).filter(stage=stage).order_by("-created_on")
    serializer = IdeaSerializer(query_set, many=True)

    result = HttpResponse(serializer.data)
    return result


# class add_category_view(CreateView):
#     model = Department
#     template_name = 'blogs/add_category.html'
#     form_class = DepartmentForm

#     def form_valid(self, form):
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(add_category_view, self).get_context_data(**kwargs)

#         return context

#     def get_success_url(self):
#         return HttpResponseRedirect(self.META.get('HTTP_REFERER', '/'))
