import re
from django.core.exceptions import ValidationError
from django.http import response
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, select_template
import smtplib, ssl
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls.base import reverse_lazy
from requests.api import head
from requests.models import HTTPBasicAuth
from .forms import AgeForm, CustomUserCreationForm, EmployeeForm, EmailForm, ProfilePic
from .decorators import  allowed_users, admin_only, unauthenticated_user
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMessage
from django.conf import Settings, settings 
from django.template.loader import render_to_string
from django.conf import settings
from .models import Account
from blog.models import Post
import random
import requests
from django.views import generic
from organisations.models import Organisation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import TokenGenerator, generate_token
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
import threading
from formtools.wizard.views import SessionWizardView, NamedUrlWizardView
import account.forms
import requests, json
import http.client
from challenges.models import Idea, Department
from django.db.models import Count
from email.mime.multipart import MIMEMultipart
from rest_framework import viewsets
from requests.auth import HTTPDigestAuth
import datetime
from django.utils.timezone import make_aware
import calendar
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from django.http.response import HttpResponseRedirect

FORMS = [("contact", account.forms.CustomUserCreationForm),
         ("age", account.forms.AgeForm),
         ("employee", account.forms.EmployeeForm)]

TEMPLATES = {"contact": "userauth/auth_username.html",
             "age": "userauth/auth_age.html",
             "employee": "userauth/auth_employee.html"}


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    

    def run(self):
        self.email.send()

@unauthenticated_user
def enter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('select_org')
        else:
            messages.info(request, 'Username OR password is incorrect')


    context = {}
    return render(request, 'userauth/enter_portal.html', context)

def logoutUser(request):
    logout(request)
    return redirect('enter')

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def home(request):
    return render(request, 'userauth/home.html')

def index(request):
    return render(request, 'userauth/index.html')

def sign_in(request):
    return render(request, 'userauth/sign_in.html')

def success(request):
    user = Account.objects.latest('date_joined')
    send_action_email(request, user=user)
    return render(request, 'userauth/success.html')

def activation_success(request):
    return render(request, 'userauth/activation_successful.html')

def auth(request):
    return render(request, 'userauth/userhub.html')

def profile_main(request, slug):  
    user = request.user
    try:
        dp = request.user.profile_image
        print(dp)
    except:
        print("Unauthenticated")
    x = 6
    now = time.localtime()
    date_list = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(x)]
    print(date_list)
    
    

    try:
        user_ideas = Idea.objects.filter(author=request.user).count()
        idea = Idea.objects.filter(author=request.user)
        stuff = Idea.total_likes_received(request.user)
        given_likes = Idea.total_likes_given(request.user)
        user_challenges = Post.objects.filter(author=request.user).count()
        wins = Idea.total_ideas_selected(request.user)
        # baseline = 3
        # score = 0
        # for i in wins:
        #     score + 0.
        baseline = 3
        score = 0
        for i in range(0,wins):
            score += 20
        print(score)
        value = round(score * 0.35)


        print(given_likes)
        print(stuff)
        print(slug)
        form = ProfilePic()
        if request.method == "POST":
            form = ProfilePic(request.POST, request.FILES,)
            if form.is_valid():
                user.profile_image = form.cleaned_data.get('profile_image')
                dp = user.profile_image
                print(dp)
                print('Succesfully saved')
                user.save()
                
                context={
                    'user':user,
                    'orgslug' : slug,
                    'dp' : dp,
                    'form':form,
        
            }

            return HttpResponseRedirect(reverse('profile_main', args=[slug]), context)
        
        context={
        'user':user,
        'total_ideas': user_ideas,
        'total_likes': stuff,
        'likes_given': given_likes,
        'total_challenges': user_challenges,
        'wins': wins,
        'score': score,
        'value': value,
        'orgslug' : slug,
        'dp' : dp,
        'form':form,
    
        }
        posts = Post.objects.filter(author=request.user).count()
        print(posts)
    except:
        context={
        'user':user,
        'orgslug' : slug,
        # 'form': form,
        }
        ValidationError("Nor signed in")
    return render(request, 'profile/profile_main.html', context)

def testing(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('Succesfully saved')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='public')
            user.groups.add(group)

            # sendEmail(username, email)
            send_action_email(request, user)

            return redirect('auth_age')

    context = {'customusercreationform': form}

    return render(request, 'blogs/regform.html', context)


def sendEmail(name, recipient):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ideasportal.nhs@gmail.com"
    password = "97_Greenwood_19"
    message = """\
    Activate your account

    Welcome to the NHS Ideas Portal """ + name          
    # message = render_to_string("emails/activate.html", name)  


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail('ideasportal.nhs@gmail.com', recipient, message)



def send_action_email(request, user):

    current_site = get_current_site(request)
    email_subject ='Activate your account'
    email_body = render_to_string('emails/activate.html', {
        'subject': email_subject,
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    msg = 'Subject: {}\n\n{}'.format(email_subject, email_body)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ideasportal.nhs@gmail.com"
    password = "shaun_ml_idea_platform_v3"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        email = server.sendmail('ideasportal.nhs@gmail.com', [user.email], msg)

    EmailThread(email).start()

def access_denied(request):
    return render(request, 'errors/access_denied.html')

# @unauthenticated_user
def auth_username(request, slug):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            group = Group.objects.get(name='public')
            signup_org = Organisation.objects.get(slug=slug)
            user.groups.add(group)
            user.affiliated_with.add(signup_org)

            return redirect('auth_age')

    context = {'customusercreationform': form}

    return render(request, 'userauth/auth_username.html', context)

def edit_email(request, slug):
    form = EmailForm()
    id = request.user.id
    user = Account.objects.get(id=id)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user.email = email
            user.save()


        return redirect('profile_main', slug=slug)

    context = {'emailform': form, 'orgslug': slug}

    return render(request, 'edit/edit_email.html', context)

def edit_profile(request, slug):
    form = ProfilePic()
    id = request.user.id
    user = Account.objects.get(id=id)
    profile_pic = user.profile_image
    if request.method == "POST":
        form = ProfilePic(request.POST)
        if form.is_valid():
            pic = form.cleaned_data.get('profile_image')
            print(pic)
            user.profile_image = pic
            user.save()


        return redirect('profile_main', slug=slug)

    context = {'form': form, 'orgslug': slug, 'pic' : profile_pic}

    return render(request, 'edit/edit_profile.html', context)

def admin_info(request):
    return render(request, 'help/admin_info.html')

def portal_manager_info(request):
    return render(request, 'help/portal_manager_info.html')

def challenge_manager_info(request):
    return render(request, 'help/challenge_manager_info.html')

def nhs_staff_info(request):
    return render(request, 'help/nhs_staff_info.html')

def public_info(request):
    return render(request, 'help/public_info.html')

def auth_number(request):
    return render(request, 'userauth/auth_number.html')

def auth_age(request):
    user = Account.objects.latest('date_joined')
    form = AgeForm()
    if request.method == "POST":
        form = AgeForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data.get('age')
            user.age = age
            user.save()

            return redirect('auth_employee')


    context = {'ageform': form}

    return render(request, 'userauth/auth_age.html', context)

def edit_age(request, slug):
    id = request.user.id
    user = Account.objects.get(id=id)
    form = AgeForm()
    if request.method == "POST":
        form = AgeForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data.get('age')
            user.age = age
            user.save()

            return redirect('profile_main', slug=slug)


    context = {'ageform': form, "orgslug" : slug}

    return render(request, 'edit/edit_age.html', context)

def auth_employee(request):
    user = Account.objects.latest('date_joined')
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            is_employee = form.cleaned_data.get('is_staff')
            if is_employee == 'Yes':
                user.is_staff = True
                user.save()
            else:
                user.save()
            return redirect('choose_interests')


    context = {'employeeform': form}
    
    return render(request, 'userauth/auth_employee.html', context)

def choose_interests(request):
    return render(request, 'userauth/choose_interests.html')

def feed(request):
    return render(request, 'blogs/base.html')

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("Your uid is: ", uid)

        user = Account.objects.get(pk=uid)
        print(user)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        print(user.is_email_verified)
        user.save()
        print("good path")

        return redirect(reverse('activation_success'))

    return render(request, 'emails/activate-failed.html', {"user": user})

# @login_required(login_url='')
def public_landing(request):
    return render(request, 'landingpages/public_landing.html')

# @login_required(login_url='')
# @allowed_users(allowed_roles=['public'])

# headers = {
#     'Content-type':'application/json', 
#     'Accept':'application/json'
# }

# headers2 = {'Authorization' : 'Bearer {access_token}'}

# url = 'https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate'

# data = {"name": "Value"}

class blogfeed_main(generic.DetailView):

    model = Organisation
    template_name = 'blogs/blogfeed_main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(blogfeed_main, self).get_context_data(*args, **kwargs)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        context['slug'] = portal_slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        context['orgslug'] = portal_slug
        today = date.today()
        six_months = today + relativedelta(months=-10)
        print(six_months)
        affiliate = []
        users = Account.objects.filter(affiliated_with=portal_choice)
        # wins = Idea.total_ideas_selected(self.request.user)
        print(users)
        ranks = []
        names = []
        score = 0

        for i in users:
            score = Idea.total_ideas_selected(i)
            ranks.append(score)
            names.append(i.username)

        print(ranks)
        print(names)
        user_data = zip(names, ranks)
        leaderboard_data = sorted(user_data)[:5]
        print(leaderboard_data)
        context['leaderboard_data'] = leaderboard_data
        total_challenges = Post.objects.filter(org_tag = portal_choice).count()
        total_ideas = Idea.objects.filter(org_tag = portal_choice).count()
        context['total_challenges'] = total_challenges
        context['total_ideas'] = total_ideas

        post_notifs = Post.objects.filter(org_tag = portal_choice).filter(author = self.request.user.id)[:5]
        idea_notifs = Idea.objects.filter(org_tag = portal_choice).filter(author = self.request.user.id)[:5]

        # notifications = zip(post_notifs, idea_notifs)
        context['notifications'] = post_notifs
        context['idea_notifications'] = idea_notifs

        has_access = False
        is_auth = False

        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        print(portal_choice)

        if self.request.user.is_authenticated:
            affiliate = self.request.user.affiliated_with.all()
            print(affiliate)
            try: 
                if portal_choice in affiliate:
                    has_access = True       
                if self.request.user.groups.filter(name = 'admins').exists():
                    has_access = True
            except:
                ValidationError("Auth issue")
        else:
            has_access = True
        
        print(has_access)
        context['has_access'] = has_access

        result = []
        year_list = []
        month_list = []
        month_name_list = []

        while today >= six_months:
            result.append(today)
            today -= relativedelta(months=1)

        for i in result:
            month_list.append(i.month)
            year_list.append(i.year)

        print(year_list)
        print(month_list)

        for i in year_list:
            print(type(i))

        for i in month_list:
            print(calendar.month_name[i])
            month_name_list.append(calendar.month_name[i].lower())

        print(month_name_list)
        month_name_list
        zipped_values = zip(month_name_list, year_list)
        context['date_list'] = zipped_values
        

        return context

    def get_success_url(self):
        pk=self.kwargs['pk']
        orgslug=self.kwargs['orgslug']
        slug = self.kwargs['slug']

        return reverse_lazy('challenge_history', kwargs={'orgslug': orgslug,})




class blogfeed_main_edit(generic.DetailView):

    form_class = Organisation
    model = Organisation
    template_name = 'blogs/blogfeed_main_edit.html'
    success_url = reverse_lazy('blogfeed_main')

    def get_context_data(self, *args, **kwargs):
        context = super(blogfeed_main_edit, self).get_context_data(*args, **kwargs)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        return context


def test_api(request):
    response = requests.post()
    affiliate = request.user.is_affilated
    print(affiliate)
    return render(request, 'home.html', {'response': response})


class ContactWizard(NamedUrlWizardView):
    template_name = 'userauth/auth_username.html'

    def done(self, form_list, **kwargs):
        form_data = self.process_form_data(self.request, form_list)
        return render('userauth/success.html', {'form_data': form_data})

    def process_form_data(form_list):
        form_data = [form.cleaned_data for form in form_list]
        username = form_data[0]['username']
        password = form_data[0]['password']
        email = form_data[0]['email']
        user = Account.objects.create_user(Account, username, email, password)
        user.save()
        return form_data


        
        

    # return render(request, 'userauth/auth_username.html', context)



# class ContactWizard(SessionWizardView):
# # template_name = 'userauth/auth_username.html'
#     def get_template_names(self):
#         return [TEMPLATES[self.steps.current]]

#     def done(self, form_list, **kwargs):
#         form_data = process_form_data(form_list)

#         return render('userauth/success.html', {'form_data': form_data})

# def process_form_data(form_list):
#     form_data = [form.cleaned_data for form in form_list]

#     return form_data