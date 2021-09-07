from django.core.exceptions import ValidationError
from django.shortcuts import render
from requests.adapters import Response
from rest_framework.views import APIView
from .forms import IdeaForm, CriteriaForm, ChallengeForm, DepartmentForm, IdeaApprovalForm
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
from django.core.paginator import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
# from rest_framework.generics import ListAPIView, CreateAPIView

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import IdeaSerializer


# Create your views here.
# def management_dashboard(request):
#     return render(request,'challenge_management/dashboard.html')

class PostList(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = 'blogs/manager_index.html'

    model = Post

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(status=0).filter(org_tag=portal_choice).filter(endDate=None).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        context['orgslug'] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

def approve_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    print(idea.status)
    idea.status = 1
    idea.stage = 'open'
    print(idea.status)
    idea.save()

    return HttpResponseRedirect(reverse('idea_management_detail', args=[orgslug, str(pk), slug]))

def reject_idea(request, pk, slug, orgslug):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    print(idea.status)
    idea.status = 0
    print(idea.status)
    idea.save()

    return HttpResponseRedirect(reverse('idea_management_detail', args=[orgslug, str(pk), slug]))

# IdeaApprovalForm

class PendingIdeasList(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = 'ideas/pending_ideas.html'
    # queryset = Idea.objects.all()

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = self.kwargs['slug']
        print(portal_choice)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        return Idea.objects.filter(status=0).filter(org_tag=portal_choice)

    def get_context_data(self, **kwargs):
        context = super(PendingIdeasList, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        context['orgslug'] = portal_slug
        


        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaManagementDetail(generic.DetailView):
    
    model = Idea
    template_name = 'ideas/idea_management_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaManagementDetail, self).get_context_data()
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        context['orgslug'] = portal_slug
        return context

class PostListCompleted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    queryset = Post.objects.filter(status=1).filter(endDate__lte=today)
    template_name = 'blogs/completed_challenges.html'

    model = Post

    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super(PostListCompleted, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        context['orgslug'] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaListOpen(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    
    queryset = Idea.objects.filter(stage='open')
    template_name = 'ideas/index_open.html'

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs['pk'])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage='open').filter(org_tag=portal_id).order_by('-created_on')
    
    def get_context_data(self, **kwargs):
        context = super(IdeaListOpen, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        print(self.kwargs['pk'])
        context['title'] = 'Open Ideas'
        context['pk'] = self.kwargs['pk']
        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaListDelivered(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    
    queryset = Idea.objects.filter(stage='delivered')
    template_name = 'ideas/index_open.html'

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs['pk'])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage='delivered').filter(org_tag=portal_id).order_by('-created_on')

    
    def get_context_data(self, **kwargs):
        context = super(IdeaListDelivered, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        print(self.kwargs['pk'])
        context['title'] = 'Delivered Ideas'
        context['pk'] = self.kwargs['pk']

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaListReview(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    
    queryset = Idea.objects.filter(stage='under review')
    template_name = 'ideas/index_open.html'

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs['pk'])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage='under review').filter(org_tag=portal_id).order_by('-created_on')

    
    def get_context_data(self, **kwargs):
        context = super(IdeaListReview, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        print(self.kwargs['pk'])
        context['title'] = 'Under-review Ideas'
        context['pk'] = self.kwargs['pk']


        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaListAccepted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    
    queryset = Idea.objects.filter(stage='accepted')
    template_name = 'ideas/index_open.html'

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs['pk'])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage='accepted').filter(org_tag=portal_id).order_by('-created_on')

    
    def get_context_data(self, **kwargs):
        context = super(IdeaListAccepted, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        print(self.kwargs['pk'])
        context['title'] = 'Accepted Ideas'
        context['pk'] = self.kwargs['pk']


        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class IdeaListInDev(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    
    queryset = Idea.objects.filter(stage='in development')
    template_name = 'ideas/index_open.html'

    model = Idea

    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(id=self.kwargs['pk'])
        portal_id = portal_choice.id
        return Idea.objects.filter(stage='in development').filter(org_tag=portal_id).order_by('-created_on')

    
    def get_context_data(self, **kwargs):
        context = super(IdeaListInDev, self).get_context_data(**kwargs) 
        list_challenges = Idea.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        print(self.kwargs['pk'])
        context['title'] = 'In-development Ideas'
        context['pk'] = self.kwargs['pk']


        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context
        
class History(generic.ListView):
    today = make_aware(datetime.datetime.now())
    template_name = 'challenges/index_history.html'

    model = Organisation
    queryset = Organisation.objects.all()
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(History, self).get_context_data(**kwargs) 
        list_challenges = Organisation.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)
        # context['slug'] = Organisation.objects.get(slug=portal_slug)
        # print(context['org'])
        context['slug'] = self.kwargs['slug']


        page = self.request.GET.get('page')

        # portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        # portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        # print(portal_choice)
        # print(portal_slug)
        # context['org'] = Organisation.objects.get(slug=portal_slug)
        # context['orgslug'] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context

class HistoryListCompleted(generic.ListView):
    today = make_aware(datetime.datetime.now())
    print(today)
    queryset = Post.objects.filter(status=1).filter(endDate__lte=today)
    template_name = 'challenges/index_completed.html'

    model = Post

    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super(HistoryListCompleted, self).get_context_data(**kwargs) 
        list_challenges = Post.objects.all()
        paginator = Paginator(list_challenges, self.paginate_by)

        page = self.request.GET.get('page')

        # portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        # portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        # print(portal_choice)
        # print(portal_slug)
        # context['org'] = Organisation.objects.get(slug=portal_slug)
        # context['orgslug'] = portal_slug

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
            
        context['list_challenges'] = file_exams
        return context    

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


def submit_challenge_successful(request, slug):
    context = { 'slug': slug}
    return render(request,'challenges/submit_challenge_success.html', context)




# def challenge_history(request):
#     return render(request,'challenges/challenge_history.html')


def submit_challenge(request, slug):
    form = ChallengeForm()
    print(slug)
    org = slug
    orgobject = Organisation.objects.get(slug=slug)
    current_site = get_current_site(request)
    print(current_site)
    print(str(current_site)[:9])
    
    if request.method == "POST":
        form = ChallengeForm(request.POST)

        # post_form = Blog
        if form.is_valid():
            form.author = request.user
            challenge = form.save()
            challenge.author = request.user
            challenge = form.save()
            Post.objects.create(author=challenge.author, title=challenge.title, severity=challenge.severity, department=challenge.department, challenge=challenge, description=challenge.description, org_tag=orgobject)

            return redirect('submit_challenge_successful', slug=slug)
    

    context = {'challengeform': form, 'org': org}



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
        
        portal_choice = Organisation.objects.get(slug=self.kwargs['orgslug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['orgslug']).slug
        print(portal_choice)
        print(portal_slug)
   

        context['challenge'] = Post.objects.get(slug=challenge_slug)
        return context
        
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        pk=self.kwargs['pk']
        orgslug=self.kwargs['orgslug']
        slug = self.kwargs['slug']
        return reverse_lazy('criteria', kwargs={'orgslug': orgslug, 'pk': pk, 'slug':slug,})

def idea_criteria_form(request, orgslug, pk, slug):
    print(pk)
    
    post = Post.objects.get(slug=slug)
    org = Organisation.objects.get(slug=orgslug)
    org_name = org.name
    print(org.name)
    publish_publicly = False
    if org_name == 'Public':
        publish_publicly = True
    # idea = Idea.objects.filter(author=request.user).latest('created_on')
    idea = Idea.objects.latest('created_on')
    print(idea)
    print(post.title)
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
            is_public = form.cleaned_data.get('is_public')
            # idea.org_tag = 
            public = Organisation.objects.get(name='Public')
            if is_public:
                idea.org_tag.add(public)


            idea.is_user_led = is_user_led
            idea.author = request.user
            idea.org_tag.add(org) 
            idea.department = post.department
            # idea.author = request.id.user
            idea.save()

            return redirect('submit_success', orgslug=orgslug, pk=pk, slug=slug)

    context = {'criteriaform': form, 'publish_publicly': publish_publicly}

    return render(request, 'ideas/idea_criteria_form.html', context)

def submit_success(request, orgslug, pk, slug):
    context = {'orgslug': orgslug}
    return  render(request, 'ideas/submit_success.html', context)

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all().order_by('title')
    serializer_class = IdeaSerializer

    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super().update(request, *args, **kwargs)

# class IdeaViewSet(viewsets.Up):
#     queryset = Idea.objects.all().order_by('title')
#     serializer_class = IdeaSerializer

    

# class IdeaAPIView(APIView):
#     serializer_class = IdeaSerializer

#     def get_queryset(self):
#         ideas = Idea.objects.all()
#         return ideas

#     def get(self, request, *args, **kwargs):
#         try:
#             id = request.query_params["id"]
#             if id != None:
#                 idea = Idea.objects.get(id=id)
#                 serializer = IdeaSerializer(idea)
#         except:
#             ideas = self.get_queryset()
#             serializer = Idea(ideas)
        
#         return Response(serializer.data)

#     def put(self, request, *args, **kwargs):
#         idea_object = Idea.object.get()

#         data = request.data 
#         idea_object.stage = data["stage"]
#         idea_object.save()
#         serializer = IdeaSerializer(idea_object)
   
#         return Response(serializer.data)
    


def lifecycle(request, pk):
    org = Organisation.objects.get(id=pk)
    org_slug = org.slug
    context = {'pk':pk, 'slug': org_slug}
    return  render(request, 'challenges/lifecycle.html', context)

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

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('bloghub')
        
