import re
from django.http import response
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, select_template
import smtplib, ssl
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls.base import reverse_lazy
from requests.api import head
from requests.models import HTTPBasicAuth
from .forms import AgeForm, CustomUserCreationForm, EmployeeForm
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
from challenges.models import Idea
from django.db.models import Count


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

def profile_main(request):
    user = request.user
    user_ideas = Idea.objects.filter(author=request.user).count()
    idea = Idea.objects.filter(author=request.user)
    stuff = Idea.total_likes_received(request.user)
    given_likes = Idea.total_likes_given(request.user)
    user_challenges = Post.objects.filter(author=request.user).count()
    print(given_likes)
    print(stuff)
    # print(Account.objects.annotate(num_likes=Count('author__likes')).order_by('-likes').filter()[:20])

    context={
      'user':user,
      'total_ideas': user_ideas,
      'total_likes': stuff,
      'likes_given': given_likes,
      'total_challenges': user_challenges,
  
    }
    posts = Post.objects.filter(author=request.user).count()
    print(posts)
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
            messages.success(request, 'Account was created for ' + username)
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

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ideasportal.nhs@gmail.com"
    password = "97_Greenwood_19"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        email = server.sendmail('ideasportal.nhs@gmail.com', [user.email], email_body)

    EmailThread(email).start()


# @unauthenticated_user
def auth_username(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            group = Group.objects.get(name='public')
            user.groups.add(group)

            return redirect('auth_age')

    context = {'customusercreationform': form}

    return render(request, 'userauth/auth_username.html', context)

# def save_contact(request):
#     form = CustomUserCreationForm()
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             print('Succesfully saved')
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             messages.success(request, 'Account was created for ' + username)
#             group = Group.objects.get(name='public')
#             user.groups.add(group)

#             # sendEmail(username, email)
#             send_action_email(user, request)

#             return redirect('auth_age')

#     context = {'customusercreationform': form}

#     return render(request, 'userauth/auth_username.html', context)



    
    
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

headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
}

url = 'https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/Token/Authenticate'

data = {"name": "Value"}

class blogfeed_main(generic.DetailView):

    model = Organisation
    template_name = 'blogs/blogfeed_main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(blogfeed_main, self).get_context_data(*args, **kwargs)
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        portal_slug = Organisation.objects.get(slug=self.kwargs['slug']).slug
        print(portal_choice)
        print(portal_slug)
        context['org'] = Organisation.objects.get(slug=portal_slug)
        return context





    # resp = requests.post(url, data={}, auth=HTTPBasicAuth('cnwl', 'K2Q5!ZqnJ!#RYV'), json=data, headers=headers)
    # print(resp)
    # print(resp.status_code)
    # print(resp.reason)
    # print(resp.content[:100])
    # for i in resp.content:
    #     print(i)
    # print(resp.headers)
    # json_store = resp.json()
    # print(resp)
    # dict = resp.json()
    # print(resp.text)
    
    # print(dict)
    # print(dict["result"])
    # please = dict["result"][0]
    # print(please)



    # fish = resp.json()
    # data_dict = json.dumps(fish)
    # print(data_dict)
    # print(data_dict["result"]["accessToken"])
    # print(resp.content)

    # print(resp.content[5])

    # url2 = "https://app-library-builder-api.orchahealth.co.uk/api/orcha/v1/SubCategory/GetSubCategories"

    # payload={}
    # headers2 = {}

    # response = requests.request("GET", url2, headers=headers2, data=payload)
    # print(response.text)
    # print(response.status_code)




    
    # post = Post.objects.all()
    # chosen_post1 = random.choice(post)
    # chosen_post2 = random.choice(post)
    # chosen_post3 = random.choice(post)

    # context = {"post1": chosen_post1,
    #             "post2": chosen_post2,
    #             "post3": chosen_post3 }

    # return render(request, "blogs/blogfeed_main.html", context)


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