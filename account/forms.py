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
        ('terrible', 'Berrible'),
        ('bad', 'Bad'),
        ('normal', 'Okay'),
        ('good', 'Good'),
        ('great', 'Great'),
    ]
    rating = forms.ChoiceField(choices = USER_RATING, widget=forms.RadioSelect, label="How would you rate your time on this site?")
    feedback_message = forms.CharField(max_length=1000, help_text='1000 characters maximum.', label="Please provide any feedback you have", required=False)
    email = forms.EmailField(max_length=254, label="If you want, please leave your email here for us to get back to you. If not, you'll remain anonymous.", required=False)

# 'interests', 'department', 'sub-department',, 'is_staff',  'is_active', 'date_joined'