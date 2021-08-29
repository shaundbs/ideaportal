from django import forms
from django.contrib.auth import get_user_model
from django.forms.fields import BooleanField
from .models import Idea, Challenge, Department, IdeaComment
from blog.models import Post

class IdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        # self.fields['department'].queryset = Department.objects.filter(is_approved=True).distinct()
        

        # self.fields['sub_department'].queryset = Department.objects.filter(is_approved=True).distinct()

    # class Meta:
    #     model = Idea
    #     fields = ['title','department', 'description', 'image']
    #     labels = {'title':'Title', 'department':'Department', 'description': 'Description', 'image' :'Image'}

    class Meta:
        model = Idea
        fields = ('title', 'description', 'image', 'department')

        

class CriteriaForm(forms.Form):
    notes = forms.CharField(label='Notes', max_length=500, widget=forms.Textarea)
    is_user_led = BooleanField()
    # image = forms.ImageField()
    estimated_cost = forms.DecimalField()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department','sub_department']
        labels = {'department':'Department', 'sub_department':'Sub-department', }

class ChallengeForm(forms.ModelForm):

    additional_field = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_approved=True)
        self.fields['additional_field'].required = False

    class Meta:
        model = Challenge
        fields = ['title','department', 'description', 'severity', 'additional_field', 'image']
        labels = {'title':'Title', 'department':'Department', 'description': 'Description', 'severity': 'Severity', 'additional_field': 'Extra', 'image':'Add an attachment'}


# class ChallengeManagementForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(ChallengeManagementForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Challenge
#         fields = ['startDate','endDate']
#         labels = {'startDate':'Start date', 'endDate':'End date'}

class PostForm(forms.ModelForm):

    additional_field = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_approved=True)
        self.fields['additional_field'].required = False

    class Meta:
        model = Post
        fields = ['title','department', 'description', 'severity', 'additional_field', 'image']
        labels = {'title':'Title', 'department':'Department', 'description': 'Description', 'severity': 'Severity', 'additional_field': 'Extra', 'image':'Add an attachment'}
    
class IdeaCommentForm(forms.ModelForm):
    class Meta:
        model = IdeaComment
        fields = ('comment', 'image')

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('startDate', 'endDate', 'status')