from django import forms
# from .models import Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.db.models.fields.files import ImageField
from django.forms import widgets
from .models import Account, Comment
from blog.models import Post
from challenges.models import Idea

class UserAuthForm(forms.Form):
    Suggestion = forms.CharField(label='Suggestion', max_length=50, widget=forms.Textarea)
    Cost_Estimate = forms.CharField(label='Cost Estimate', max_length=30,widget=forms.Textarea)
    Plan = forms.CharField(label='Plan', max_length=30,widget=forms.Textarea)

class CreateUserForm(UserCreationForm):
    class Meta:
        # model = get
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'image')



    

    # widgets = {
    #     'comment': forms.Textarea(attrs='class' : 'form-control'),
    # }


    # comment = forms.CharField(label='Comment', max_length=500, widget=forms.Textarea)
    # image = forms.ImageField(allow_empty_file=True)


# 'interests', 'department', 'sub-department',, 'is_staff',  'is_active', 'date_joined'

