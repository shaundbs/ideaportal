from django import forms
# from .models import Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from django.db.models.fields.files import ImageField
from .models import Account


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email']

class EmailForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email',)

class ProfilePic(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('profile_image',)
    
        
class AgeForm(forms.Form):
    AGE_RANGES = [
    ('16-20', '16-20'),
    ('21-30', '21-30'),
    ('31-40', '31-40'),
    ('41-50', '41-50'),
    ('51-65', '51-65'),
    ('65+', '65+'),
]
    age = forms.ChoiceField(choices=AGE_RANGES, widget=forms.RadioSelect)

class EmployeeForm(forms.Form):
    BOOLEAN = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
    is_staff = forms.ChoiceField(choices=BOOLEAN, widget=forms.RadioSelect)

    
class FeedbackForm(forms.Form):
    USER_RATING = [
        ('terrible', 'Completely Dissatisfying'),
        ('bad', 'Disatisfying'),
        ('normal', 'Neutral'),
        ('good', 'Satisfying'),
        ('great', 'Completely Satisfying'),
    ]

    EASE_OF_USE_RATING = [
        ('terrible', 'I need someone to show me how to use the site'),
        ('bad', 'I need someone to show me how to use certain features'),
        ('normal', 'It will take me a few uses to learn how to use the site'),
        ('good', 'Next time I use it, I’ll know exactly what to do'),
        ('great', 'I felt like I’ve been using it all my life'),
    ]

    experience_rating = forms.ChoiceField(choices = USER_RATING, widget=forms.RadioSelect, label="How would you rate your overall experience on our site?")
    use_rating = forms.ChoiceField(choices = USER_RATING, widget=forms.RadioSelect, label="How easy was the site to use?")
    improvement_message = forms.CharField(max_length=1000, help_text='1000 characters maximum.', label="What can we do to make the Ideas Portal better?", required=False)
    next_feature_message = forms.CharField(max_length=1000, help_text='1000 characters maximum.', label="What’s the next feature we should build?", required=False)
    feedback_message = forms.CharField(max_length=1000, help_text='1000 characters maximum.', label="Please provide any other feedback you have", required=False)
    email = forms.EmailField(max_length=254, label="If you want, please leave your email here for us to get back to you. If not, you'll remain anonymous.", required=False)

# 'interests', 'department', 'sub-department',, 'is_staff',  'is_active', 'date_joined'