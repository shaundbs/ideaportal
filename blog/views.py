from os import stat, stat_result
from re import S
import re

import challenges.models
from challenges.forms import DepartmentForm, IdeaCommentForm, ApprovalForm
from challenges.models import Idea, IdeaComment, Department
from django.contrib import messages
from django.core.checks import messages
from django.core.paginator import *
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
import requests
from organisations.models import Organisation
from django.db.models import Max, Count
from .forms import CommentForm
from .models import Comment, Post
from organisations.models import Organisation
from django.db import models
from django.utils.timezone import make_aware
import datetime
from account.decorators import has_org_access
from challenges.models import OrgForm
import logging

from ideaportal.templates import ListViewTemplate


def search_blog(request, slug):
    # org = Organisation.objects.get(id=slug)
    orgslug = slug
    orgid = Organisation.objects.filter(slug=orgslug)[0].id

    if request.method == "POST":
        searched = request.POST["searched"]
        posts = Post.objects.filter(title__icontains=searched, org_tag=orgid)
        ideas = Idea.objects.filter(title__icontains=searched, org_tag=orgid)
        # contents no use
        contents = Post.objects.filter(description__icontains=searched)
        logging.error("hello")

        return render(
            request,
            "search/blog_search.html",
            {
                "searched": searched,
                "posts": posts,
                "ideas": ideas,
                "contents": contents,
                "orgslug": orgslug,
            },
        )
    else:
        return render(request, "search/blog_search.html", {})


def search_idea(request, orgslug, pk, slug):
    if request.method == "POST":
        searched = request.POST["searched"]
        post = Post.objects.get(id=pk)

        ideas = Idea.objects.filter(post=post).filter(title__icontains=searched)

        return render(
            request,
            "search/idea_search.html",
            {
                "searched": searched,
                "ideas": ideas,
                "orgslug": orgslug,
                "pk": pk,
                "slug": slug,
            },
        )
    else:
        return render(request, "search/idea_search.html", {})


class MyDetailView(generic.DetailView):
    model = Post
    template_name = "blogs/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MyDetailView, self).get_context_data(*args, **kwargs)
        context["comment_list"] = Comment.objects.all()
        return context


class PostList(ListViewTemplate):
    """The view of the list of challenges"""

    template_name = "blogs/index_latestpoll.html"
    model = Post
    paginate_by = 4

    def _filter_queryset(self, queryset):
        return queryset.filter(status=1).order_by("-created_on" ,"-updated_on")


class PostListHealth(PostList):

    template_name = "blogs/index_health.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Health").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostListOrgSpecific(PostList):

    template_name = "blogs/index_org_specific.html"


class PostListMonth(PostList):

    template_name = "blogs/index_archives.html"

    def get_queryset(self, *args, **kwargs):
        datetime_object = datetime.datetime.strptime(self.kwargs["month"], "%B")
        return super().get_queryset(*args, **kwargs).filter(created_on__month = datetime_object.month)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = self.kwargs["month"]
        return context


class PostListCulture(PostList):

    template_name = "blogs/index_culture.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Culture").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostListJobSatisfaction(PostList):

    template_name = "blogs/index_job_sat.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Job Satisfaction").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostListRelationships(PostList):

    template_name = "blogs/index_relationships.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Relationships").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostListLeadership(PostList):

    template_name = "blogs/index_leadership.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Leadership").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostListData(PostList):

    template_name = "blogs/index_data.html"

    def get_queryset(self, *args, **kwargs):
        dept_id = Department.objects.get(department="Data").id
        return super().get_queryset(*args, **kwargs).filter(department=dept_id)


class PostDetail(generic.DetailView):
    model = Post
    template_name = "blogs/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()
        all_ideas = Idea.objects.filter(post=self.kwargs["pk"]).order_by("-likes")
        context["total_ideas"] = all_ideas.count()

        try:
            winning_idea = all_ideas.order_by("likes")[:1]
            winning_idea_id = winning_idea.values("id")[0]["id"]
            winning_idea_slug = winning_idea.values("slug")[0]["slug"]
            logging.error(winning_idea_slug)
            context["winnerpk"] = winning_idea_id
            context["winnerslug"] = winning_idea_slug
            stuff.winner = Idea.objects.get(id=winning_idea_id)
            stuff.save()
            logging.error(stuff.winner)
        except:
            logging.error("fail")

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug
        context["orgslug"] = portal_slug

        return context


class PostCommentList(generic.ListView):
    model = Comment
    template_name = "components/sidebar_challenge.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostCommentList, self).get_context_data()

        stuff = get_object_or_404(Comment, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs["slug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["slug"]).slug
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["org"] = Organisation.objects.get(slug=portal_slug)

        return context


def approve_challenge(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    logging.error(post.status)
    post.status = True
    logging.error(post.status)
    post.save()

    return HttpResponseRedirect(reverse("pending_idea", args=[orgslug, str(pk), slug]))


def add_dates(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    logging.error(post.status)
    post.status = True
    logging.error(post.status)
    post.save()

    return HttpResponseRedirect(reverse("post_management_detail", args=[str(pk), slug]))


def reject_challenge(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    logging.error(post.status)
    post.status = False
    logging.error(post.status)
    post.save()

    return HttpResponseRedirect(reverse("post_management_detail", args=[orgslug, str(pk), slug]))


def like_view(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    logging.error(post.slug)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("post_detail", args=[orgslug, str(pk), slug]))


def like_view_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get("idea_id"))

    liked = False
    if idea.likes.filter(id=request.user.id).exists():
        idea.likes.remove(request.user)
        liked = False
    else:
        idea.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("idea_post", args=[orgslug, str(pk), slug]))


def approval_view(request, pk, slug, orgslug):
    logging.error(pk)
    form = ApprovalForm()
    post = Post.objects.get(id=pk)
    logging.error(post.title)
    if request.method == "POST":
        form = ApprovalForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data.get("startDate")
            logging.error(startDate)
            endDate = form.cleaned_data.get("endDate")
            logging.error(endDate)
            status = form.cleaned_data.get("status")
            logging.error(status)
            post.startDate = startDate
            post.endDate = endDate
            post.status = status
            post.stage = "open"
            post.save()

            return redirect("post_management_detail", orgslug=orgslug, pk=pk, slug=slug)

        context = {"approvalform": form}

    return render(request, "blogs/approval.html", context)


class comment_view(CreateView):
    model = Comment
    template_name = "blogs/comment.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(comment_view, self).get_context_data()
        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug

        post = Post.objects.get(slug=self.kwargs["slug"])
        title = post.title
        desc = post.description

        logging.error(portal_choice)
        logging.error(portal_slug)
        context["orgslug"] = portal_slug
        context["description"] = desc
        context["title"] = title

        return context

    def get_success_url(self):
        logging.error(self.kwargs["orgslug"])
        return reverse_lazy(
            "post_detail",
            kwargs={
                "orgslug": self.kwargs["orgslug"],
                "pk": self.kwargs["pk"],
                "slug": self.kwargs["slug"],
            },
        )


def search_idea_page(request, orgslug, pk, slug):
    return render(request, "blogs/searchidea.html")


class idea_comment_view(CreateView):
    model = IdeaComment
    template_name = "blogs/idea_comment.html"
    form_class = IdeaCommentForm

    def form_valid(self, form):
        stuff = get_object_or_404(Idea, id=self.kwargs["pk"])
        form.instance.post_id = self.kwargs["pk"]
        form.instance.author = self.request.user
        form.instance.idea = stuff
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(idea_comment_view, self).get_context_data()

        stuff = get_object_or_404(Idea, id=self.kwargs["pk"])
        context["posty"] = stuff.slug
        context["postid"] = stuff.pk
        total_likes = stuff.total_likes()
        title = stuff.title
        desc = stuff.description
        context["description"] = desc
        context["title"] = title

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug

        logging.error(stuff.slug)
        logging.error(portal_choice)
        logging.error(portal_slug)
        context["orgslug"] = portal_slug

        return context

    def get_success_url(self):
        logging.error(self.kwargs["orgslug"])
        return reverse_lazy(
            "idea_post",
            kwargs={
                "orgslug": self.kwargs["orgslug"],
                "pk": self.kwargs["pk"],
                "slug": self.kwargs["slug"],
            },
        )


class IdeaDetail(generic.DetailView):
    model = Idea
    template_name = "blogs/idea_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaDetail, self).get_context_data()
        stuff = get_object_or_404(Idea, id=self.kwargs["pk"])

        idea_pk = stuff.pk
        logging.error(self.kwargs["pk"])
        context["pk"] = idea_pk

        idea_comments = IdeaComment.objects.filter(idea=self.kwargs["pk"])
        logging.error(idea_comments)
        context["idea_comments"] = idea_comments

        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["liked"] = liked

        portal_choice = Organisation.objects.get(slug=self.kwargs["orgslug"])
        logging.error(portal_choice)

        portal_slug = Organisation.objects.get(slug=self.kwargs["orgslug"]).slug
        logging.error(portal_slug)
        context["orgslug"] = portal_slug

        idea_pridar = stuff.is_pridar
        context["custom"] = idea_pridar
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

        return context


class SelectedIdeaDetail(generic.DetailView):
    model = Idea
    template_name = "blogs/selected_idea_detail.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SelectedIdeaDetail, self).get_context_data()

    #     stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
    #     idea_post = stuff.post.slug
    #     idea_pk = stuff.post.id
    #     logging.error(idea_post)
    #     context['slug'] = idea_post
    #     context['pk'] = idea_pk
    #     logging.error(self.kwargs['pk'])
    #     idea_comments = IdeaComment.objects.filter(idea=self.kwargs['pk'])
    #     logging.error(idea_comments)
    #     context['idea_comments'] = idea_comments

    #     total_likes = stuff.total_likes()

    #     liked = False
    #     if stuff.likes.filter(id=self.request.user.id).exists():
    #         liked = True

    #     context["total_likes"] = total_likes
    #     context["liked"] = liked

    # return context
