from django.shortcuts import render
from .forms import IdeaForm, CriteriaForm, ChallengeForm, DepartmentForm
from django.shortcuts import redirect
from operator import pos
from django.core.checks import messages
from django.http.response import HttpResponseRedirect
from django.views import generic
from .models import Challenge, Post, Idea, Department
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from organisations.models import Organisation

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



# Create your views here.
# def management_dashboard(request):
#     return render(request,'challenge_management/dashboard.html')

class PostList(generic.ListView):
    today = make_aware(datetime.datetime.now())
    queryset = Post.objects.filter(status=0).filter(endDate=None).order_by('-created_on')
    template_name = 'blogs/manager_index.html'

    model = Post

class PostListCompleted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    queryset = Post.objects.filter(status=1).filter(endDate__lte=today)
    # most_popular = Idea.objects.order_by("-likes")[:3]
    # print(most_popular)
    template_name = 'blogs/completed_challenges.html'

    model = Post

    

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PostList, self).get_context_data()

    #     stuff = get_object_or_404(Post, id=self.kwargs['pk'])
    #     total_likes = stuff.total_likes()

    #     liked = False
    #     if stuff.likes.filter(id=self.request.user.id).exists():
    #         liked = True

    #     context["total_likes"] = total_likes
    #     context["liked"] = liked

    #     return context


def submit_challenge_successful(request):
    return render(request,'challenges/submit_challenge_success.html')


def challenge_history(request):
    return render(request,'challenges/challenge_history.html')


def submit_challenge(request):
    form = ChallengeForm()
    if request.method == "POST":
        form = ChallengeForm(request.POST)

        # post_form = Blog
        if form.is_valid():
            form.author = request.user
            challenge = form.save()
            challenge.author = request.user
            challenge = form.save()
            Post.objects.create(author=challenge.author, title=challenge.title, severity=challenge.severity, department=challenge.department, challenge=challenge, description=challenge.description)

            return redirect('submit_challenge_successful')

    context = {'challengeform': form}

    return render(request,'challenges/submit_challenge.html', context)

# def ideaform(request):
#     form = IdeaForm()
#     if request.method == "POST":
#         form = IdeaForm(request.POST, request.FILES)
#         if form.is_valid():
#             idea = form.save()
#             return redirect('criteria')

#     context = {'ideaform': form}

#     return render(request, 'ideas/submit_ideas_form.html', context)

class ideaform(CreateView):
    model = Idea
    template_name = 'ideas/submit_ideas_form.html' 
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(ideaform, self).get_context_data(**kwargs)
        obj = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['object'] = context['post'] = obj
        challenge_choice = Post.objects.get(slug=self.kwargs['slug'])
        challenge_slug = Post.objects.get(slug=self.kwargs['slug']).slug
        print(challenge_slug)
        context['challenge'] = Post.objects.get(slug=challenge_slug)
        return context
        
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        # form.instance.department = self.get_context_data.
        # form.instance.post_department = self.get_context_data(['post.department'])
        return super().form_valid(form)

    

    # def get_context_data(self, **kwargs):
    #     context = super(ideaform, self).get_context_data(**kwargs)
    #     context['idea'] = Post.objects.get(department=self.kwargs['department'])
    #     return context

    success_url = reverse_lazy('criteria')

# class ideaform(CreateView):
#     model = Idea
#     template_name = 'blogs/submit_ideas_form.html' 
#     form_class = IdeaForm

#     def form_valid(self, form):
#         form.instance.post_id = self.kwargs['pk']
#         form.instance.slug = self.kwargs['slug']

#         return super().form_valid(form)

#     success_url = reverse_lazy('bloghub')
    
# class idea_criteria_form(CreateView):

#     model = Idea
#     template_name = 'ideas/idea_criteria_form.html' 
#     form_class = CriteriaForm()

#     def form_valid(self, form):
#         form.instance.post_id = self.kwargs['pk']
#         return super().form_valid(form)

#     success_url = ('submit_success')


    # idea = Idea.objects.latest('created_on')
    # form = CriteriaForm()
    # if request.method == "POST":
    #     form = CriteriaForm(request.POST)
    #     if form.is_valid():
    #         estimated_cost = form.cleaned_data.get('estimated_cost')
    #         print(estimated_cost)
    #         idea.estimated_cost = estimated_cost
    #         notes = form.cleaned_data.get('notes')
    #         idea.notes = notes
    #         is_user_led = form.cleaned_data.get('is_user_led')
    #         idea.is_user_led = is_user_led
            # idea.author = request.id.user
            # idea.save()

def idea_criteria_form(request):
    idea = Idea.objects.latest('created_on')
    form = CriteriaForm()
    if request.method == "POST":
        form = CriteriaForm(request.POST)
        if form.is_valid():
            estimated_cost = form.cleaned_data.get('estimated_cost')
            print(estimated_cost)
            idea.estimated_cost = estimated_cost
            notes = form.cleaned_data.get('notes')
            idea.notes = notes
            is_user_led = form.cleaned_data.get('is_user_led')
            idea.is_user_led = is_user_led
            idea.author = request.user
            # idea.author = request.id.user
            idea.save()

            return redirect('submit_success')

    context = {'criteriaform': form}

    return render(request, 'ideas/idea_criteria_form.html', context)

def submit_success(request):
    return  render(request, 'ideas/submit_success.html')

class CommentList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blogs/index.html'
    

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

        return context

    
class add_category_view(CreateView):
    model = Department
    template_name = 'blogs/add_category.html' 
    form_class = DepartmentForm

    # def form_valid(self, form):
    #     form.instance.post_id = self.kwargs['pk']
    #     return super().form_valid(form)

    success_url = reverse_lazy('bloghub')
        
