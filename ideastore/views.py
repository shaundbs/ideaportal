from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.core.paginator import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

from organisations.models import Organisation
from challenges.models import Idea, OrgForm
from challenges.forms import IdeaForm, PRIDARForm, CriteriaForm
from .forms import EnhancedIdeaForm

import logging
import requests, json

# Create your views here.


def view_ideas():
    pass


class SubmitIdea(CreateView):
    """The view for submitting challenge less idea"""

    model = Idea
    template_name = "ideastore/submit_idea_without_challenge.html"
    form_class = EnhancedIdeaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        has_access = False
        if self.request.user.is_authenticated:
            has_access = True
        context["has_access"] = has_access
        context["custom_on"] = is_pridar

        context
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        orgslug = self.kwargs["orgslug"]
        return reverse_lazy("idea_criteria", kwargs={"orgslug": orgslug})


def idea_criteria_form(request, orgslug):
    """This function need to be refactor to a class so it could be inherit
    from challenges.views.idea_criteria_form
    """
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
    is_pridar = current_idea.is_pridar
    # is_pridar = org.custom_form_on
    logging.error(is_pridar)
    if is_pridar is True:
        form = PRIDARForm()
        if activate_api:
            # authentication credential for ORCHA API
            data = '{"username" : "cnwl", "password":"K2Q5!ZqnJ!#RYV"}'

            # header configuration to define format of data
            headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
            }

            # authentication end point call to generate an access token to peform other REST API calls
            response = requests.post(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate",
                data=data,
                headers=headers,
            )
            # create a JSON from the string generated from the response
            body = json.loads(response.text)
            # parse the JSON to extract the access token and save as its own variable
            access_token = body["result"]["accessToken"]

            # configure another header that uses the access token from the authentication end point
            headers_2 = {"Authorization": "Bearer " + str(access_token)}
            headers_3 = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + str(access_token),
            }
            # sub-category endpoint call to extract all categories that ORCHA use to define its applications
            response_2 = requests.get(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories",
                headers=headers_2,
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

            if (set(category_list_lower) & set(title_list_lower)) & set(
                description_list_lower
            ):
                logging.info("This idea could be similar to an exisiting solution")
                is_similar = True
                logging.info("MATCH ALERT")
                category_names = list(
                    set(category_list_lower)
                    & set(title_list_lower)
                    & set(description_list_lower)
                )
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
                    "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Review/SearchPagedReviews",
                    data=data_2,
                    headers=headers_3,
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

                zipped_values = zip(
                    existing_idea_names,
                    existing_publisher_names,
                    existing_descriptions,
                    existing_links,
                    exisiting_platforms,
                )
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
                pridar_idea.author = request.user
                current_idea.author = request.user
                pridar_idea.post = current_idea.post
                current_idea.org_tag.add(org)
                """Issue, add department selection to idea submit form 01"""
                # current_idea.department = post.department
                pridar_idea.org_tag.add(org)
                # pridar_idea.department = post.department
                estimated_cost = form.cleaned_data.get("estimated_cost")
                notes = form.cleaned_data.get("notes")
                pridar_idea.notes = notes
                current_idea.notes = notes
                is_user_led = form.cleaned_data.get("is_user_led")
                is_public = form.cleaned_data.get("is_public")
                public = Organisation.objects.get(name="Public")
                pridar_idea.save()
                current_idea.save()

                return redirect("submit_success", orgslug=orgslug)

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
            context = {
                "criteriaform": form,
                "publish_publicly": publish_publicly,
            }

        return render(request, "ideas/idea_orgspecific_form.html", context)
    else:
        form = CriteriaForm()
        if activate_api:
            data = '{"username" : "cnwl", "password":"K2Q5!ZqnJ!#RYV"}'

            headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
            }

            response = requests.post(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate",
                data=data,
                headers=headers,
            )
            body = json.loads(response.text)
            access_token = body["result"]["accessToken"]
            # logging.error(response.headers)
            # logging.error(access_token)

            headers_2 = {"Authorization": "Bearer " + str(access_token)}
            headers_3 = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + str(access_token),
            }
            # logging.error(headers_2)
            response_2 = requests.get(
                "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories",
                headers=headers_2,
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
                    "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Review/SearchPagedReviews",
                    data=data_2,
                    headers=headers_3,
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

                zipped_values = zip(
                    existing_idea_names,
                    existing_publisher_names,
                    existing_descriptions,
                    existing_links,
                    exisiting_platforms,
                )
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
                current_idea.author = request.user
                current_idea.org_tag.add(org)
                """Issue, add department selection to idea submit form 01"""
                # current_idea.department = post.department
                current_idea.save()

                return redirect("idea_submit_success", orgslug=orgslug)

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
            context = {
                "criteriaform": form,
                "publish_publicly": publish_publicly,
            }

        return render(request, "ideas/idea_criteria_form.html", context)


def submit_success(request, orgslug):
    context = {"orgslug": orgslug}
    return render(request, "ideas/submit_success.html", context)


class IdeaList(generic.ListView):
    """The view for ideastore, which the page that shows all the ideas"""

    model = Idea
    paginate_by = 4
    template_name = "ideastore/idea_list.html"
    context_object_name = "ideas"

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
        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        return Idea.objects.filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_ideas = Idea.objects.all()
        paginator = Paginator(list_ideas, self.paginate_by)

        page = self.request.GET.get("page")

        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        context["org"] = Organisation.objects.get(slug=portal_slug)

        spec_on = False
        custom_form_on = portal_choice.custom_form_on
        if custom_form_on:
            spec_on = True

        context["spec_on"] = spec_on

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context["list_challenges"] = file_exams
        return context


class IdeaListHealth(IdeaList):
    template_name = "ideastore/idea_list_health.html"


class IdeaListCulture(IdeaList):
    template_name = "ideastore/idea_list_culture.html"


class IdeaListJobSatifiction(IdeaList):
    template_name = "ideastore/idea_list_job_sat.html"


class IdeaListRelationships(IdeaList):
    template_name = "ideastore/idea_list_relationships.html"


class IdeaListLeadership(IdeaList):
    template_name = "ideastore/idea_list_leadership.html"


class IdeaListData(IdeaList):
    template_name = "ideastore/idea_list_data.html"


class IdeaListPridar(IdeaList):
    template_name = "ideastore/idea_list_pridar.html"


class IdeaListMonth(IdeaList):
    template_name = "ideastore/idea_list_archives.html"
