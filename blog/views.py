from os import stat, stat_result

import challenges.models
from challenges.forms import DepartmentForm, IdeaCommentForm, ApprovalForm
from challenges.models import Idea, IdeaComment
from django.contrib import messages
from django.core.checks import messages
from django.core.paginator import *
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
import requests
from organisations.models import Organisation

from .forms import CommentForm
from .models import Comment, Post


def search_blog(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        contents = Post.objects.filter(description__contains=searched)


        return render(request, 'search/blog_search.html', {'searched': searched, 'posts': posts, 'contents': contents})
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
    

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
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

        context["total_likes"] = total_likes
        context["liked"] = liked
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)

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

def approve_challenge(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = True
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[str(pk), slug]))


def add_dates(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = True
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[str(pk), slug]))

def reject_challenge(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    print(post.status)
    post.status = False
    print(post.status)
    post.save()

    return HttpResponseRedirect(reverse('post_management_detail', args=[str(pk), slug]))

def like_view(request, pk, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk), slug]))

def like_view_idea(request, pk, slug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    liked = False
    if idea.likes.filter(id=request.user.id).exists():
        idea.likes.remove(request.user)
        liked = False
    else:
        idea.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('idea_post', args=[str(pk), slug]))

class approval_view(CreateView):
    model = Post
    template_name = 'blogs/approval.html' 
    form_class = ApprovalForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('bloghub')

class comment_view(CreateView):
    model = Comment
    template_name = 'blogs/comment.html' 
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('bloghub')

class idea_comment_view(CreateView):
    model = IdeaComment
    template_name = 'blogs/idea_comment.html' 
    form_class = IdeaCommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('bloghub')


class IdeaDetail(generic.DetailView):
    model = Idea
    template_name = 'blogs/idea_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaDetail, self).get_context_data()

        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked

        return context

