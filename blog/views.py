from os import stat, stat_result
from re import S
import re

import challenges.models
from challenges.forms import DepartmentForm, IdeaCommentForm, ApprovalForm
from challenges.models import Idea, IdeaComment
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


def search_blog(request, slug):
    # org = Organisation.objects.get(id=slug)
    orgslug = slug

    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        contents = Post.objects.filter(description__contains=searched)
        # print(orgslug)
        print("hello")

        

        return render(request, 'search/blog_search.html', {'searched': searched, 'posts': posts, 'contents': contents, 'orgslug' : orgslug,})
    else:
        return render(request, 'search/blog_search.html', {})

def search_idea(request):
    if request.method == "POST":
        searched = request.POST['searched']
        ideas = Idea.objects.filter(title__contains=searched)
        

        return render(request, 'search/idea_search.html', {'searched': searched, 'ideas': ideas})
    else:
        return render(request, 'search/idea_search.html', {})


class MyDetailView(generic.DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyDetailView, self).get_context_data(*args, **kwargs)
        context['comment_list'] = Comment.objects.all()
        return context

class PostList(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        context['org'] = Organisation.objects.get(slug=portal_slug)
        print(context['org'].slug)
        
        


        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListHealth(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_health.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=1)

    def get_context_data(self, **kwargs):
        context = super(PostListHealth, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListMonth(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_archives.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        datetime_object = datetime.datetime.strptime(self.kwargs['month'], "%B")
        print(datetime_object.month)
        print(datetime_object)
        return Post.objects.filter(org_tag=portal_choice).filter(created_on__month = datetime_object.month).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super(PostListMonth, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        datetime_object = datetime.datetime.strptime(self.kwargs['month'], "%B")
        print(datetime_object.month)
        print(datetime_object)
        context['month'] = self.kwargs['month']
        
     




        

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        context['orgslug'] = portal_slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListCulture(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_culture.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=2)

    def get_context_data(self, **kwargs):
        context = super(PostListCulture, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListJobSatisfaction(generic.ListView):
    paginate_by = 1
    template_name = 'blogs/index_job_sat.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=3)

    def get_context_data(self, **kwargs):
        context = super(PostListJobSatisfaction, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListRelationships(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_relationships.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=4)

    def get_context_data(self, **kwargs):
        context = super(PostListRelationships, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListLeadership(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_leadership.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=7)

    def get_context_data(self, **kwargs):
        context = super(PostListLeadership, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class PostListData(generic.ListView):
    paginate_by = 4
    template_name = 'blogs/index_data.html'

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=1).filter(org_tag=portal_choice).filter(department=5)

    def get_context_data(self, **kwargs):
        context = super(PostListData, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context
    

# def get_winning_idea():
#     for idea in all_ideas:
#                 print(idea.total_likes())

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'


    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        all_ideas = Idea.objects.filter(post=self.kwargs['pk'])
        context["total_ideas"] = all_ideas.count()

        try:
            winning_idea = all_ideas.order_by("likes")[:1]
            winning_idea_id = winning_idea.values('id')[0]['id']
            winning_idea_slug = winning_idea.values('slug')[0]['slug']
            print(winning_idea_slug)
            context['winnerpk'] = winning_idea_id
            context['winnerslug'] = winning_idea_slug
        except:
            print("hello")

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        context['orgslug'] = portal_slug

        return context

        

class PostManagementDetail(generic.DetailView):
    
    model = Post
    template_name = 'blogs/post_management_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostManagementDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        # today = datetime.date.today()
        # print(today)
        active = False
        
        if stuff.endDate == None:
            active = True



        context["total_likes"] = total_likes
        context["liked"] = liked
        context["is_active"] = active

        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        context['orgslug'] = portal_slug
        return context

class PostCommentList(generic.ListView):
    model = Comment
    template_name = 'components/sidebar_challenge.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostCommentList, self).get_context_data()

        stuff = get_object_or_404(Comment, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

        return context

def approve_challenge(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = True
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[orgslug, str(pk), slug]))


def add_dates(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = True
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[str(pk), slug]))

def reject_challenge(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = False
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[orgslug, str(pk), slug]))

def like_view(request, pk, slug, orgslug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.slug)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post_detail', args=[orgslug, str(pk), slug]))

def like_view_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))

    liked = False
    if idea.likes.filter(id=request.user.id).exists():
        idea.likes.remove(request.user)
        liked = False
    else:
        idea.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('idea_post', args=[orgslug, str(pk), slug]))

def approval_view(request, pk, slug, orgslug):
    print(pk)
    form = ApprovalForm()
    idea = Post.objects.get(id=pk)
    print(idea.title)
    if request.method == "POST":
        form = ApprovalForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data.get('startDate')
            print(startDate)
            endDate = form.cleaned_data.get('endDate')
            print(endDate)
            status = form.cleaned_data.get('status')
            print(status)
            idea.startDate = startDate
            idea.endDate = endDate
            idea.status = status
            idea.stage = 'open'
            idea.save()

            return redirect('post_management_detail', orgslug=orgslug, pk=pk, slug=slug)

        context = {'approvalform': form}

    return render(request, 'blogs/approval.html', context)

# class approval_view(CreateView):
#     model = Post
#     template_name = 'blogs/approval.html' 
#     form_class = ApprovalForm

    # def form_valid(self, form):
    #     form.instance.post_id = self.kwargs['pk']
    #     return super().form_valid(form)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PostCommentList, self).get_context_data()

    #     stuff = get_object_or_404(Comment, id=self.kwargs['pk'])
    #     total_likes = stuff.total_likes()

        # liked = False
        # if stuff.likes.filter(id=self.request.user.id).exists():
        #     liked = True

        # context["total_likes"] = total_likes
        # context["liked"] = liked
        # portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        # portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        # print(portal_choice)
        # print(portal_slug)
        # context['org'] = Organisation.objects.get(slug=portal_slug)

        # return context

    success_url = reverse_lazy('profile_main')

class comment_view(CreateView):
    model = Comment
    template_name = 'blogs/comment.html' 
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(comment_view, self).get_context_data()
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug

        post = Post.objects.get(slug=self.kwargs['slug'])
        title = post.title
        desc = post.description

        print(portal_choice)
        print(portal_slug)
        context['orgslug'] = portal_slug
        context['description'] = desc
        context['title'] = title



        return context

    def get_success_url(self):
        print(self.kwargs['orgslug'])
        return reverse_lazy('post_detail', kwargs={'orgslug': self.kwargs['orgslug'], 'pk' : self.kwargs['pk'], 'slug' : self.kwargs['slug'] })


class idea_comment_view(CreateView):
    model = IdeaComment
    template_name = 'blogs/idea_comment.html' 
    form_class = IdeaCommentForm

    def form_valid(self,form):
        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        form.instance.idea = stuff
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(idea_comment_view, self).get_context_data()

        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        context['posty'] = stuff.slug
        context['postid'] = stuff.pk
        total_likes = stuff.total_likes()


        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug

        print(stuff.slug)
        print(portal_choice)
        print(portal_slug)
        context['orgslug'] = portal_slug

        return context

    def get_success_url(self):
        print(self.kwargs['orgslug'])
        return reverse_lazy('idea_post', kwargs={'orgslug': self.kwargs['orgslug'], 'pk' : self.kwargs['pk'], 'slug' : self.kwargs['slug'] })



class IdeaDetail(generic.DetailView):
    model = Idea
    template_name = 'blogs/idea_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaDetail, self).get_context_data()

        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        idea_post = stuff.post.slug
        idea_pk = stuff.post.id
        print(idea_post)
        context['slug'] = idea_post
        context['pk'] = idea_pk
        print(self.kwargs['pk'])
        idea_comments = IdeaComment.objects.filter(idea=self.kwargs['pk'])
        print(idea_comments)
        context['idea_comments'] = idea_comments


        total_likes = stuff.total_likes()


        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        print(portal_choice)
        print(portal_slug)
        context['orgslug'] = portal_slug

        return context

class SelectedIdeaDetail(generic.DetailView):
    model = Idea
    template_name = 'blogs/selected_idea_detail.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(SelectedIdeaDetail, self).get_context_data()

    #     stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
    #     idea_post = stuff.post.slug
    #     idea_pk = stuff.post.id
    #     print(idea_post)
    #     context['slug'] = idea_post
    #     context['pk'] = idea_pk
    #     print(self.kwargs['pk'])
    #     idea_comments = IdeaComment.objects.filter(idea=self.kwargs['pk'])
    #     print(idea_comments)
    #     context['idea_comments'] = idea_comments

    #     total_likes = stuff.total_likes()

    #     liked = False
    #     if stuff.likes.filter(id=self.request.user.id).exists():
    #         liked = True

    #     context["total_likes"] = total_likes
    #     context["liked"] = liked
  

        # return context



