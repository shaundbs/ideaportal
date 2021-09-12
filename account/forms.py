from django import forms
# from .models import Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth import get_user_model
from .models import Account


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email']

class EmailForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email',)

        
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

    


# 'interests', 'department', 'sub-department',, 'is_staff',  'is_active', 'date_joined'