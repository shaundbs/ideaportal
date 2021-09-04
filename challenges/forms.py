from django import forms
from django.forms import  widgets
from django.contrib.auth import get_user_model
from django.forms.fields import BooleanField
from .models import Idea, Challenge, Department, IdeaComment
from blog.models import Post
import datetime
from django.utils.timezone import make_aware

class IdeaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        # self.fields['department'].queryset = Department.objects.filter(is_approved=True).distinct()
        # self.fields['department'].required = True

        
    #     class TaskForm(forms.ModelForm):
    # class Meta:
    #     model = Task

    # def handle_state(self, *args, **kwargs):
    #     task = getattr(self, 'instance', None)
    #     if task:     
    #         if task.status = Task.ACCEPTED:
    #              self.fields['datereceived'].disabled = True
    #          elif task.status = Task.COMPLETED:
    #              ...

    # def __init__(self, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)
    #     self.handle_state(*args, **kwargs)   

        # self.fields['sub_department'].queryset = Department.objects.filter(is_approved=True).distinct()

    # class Meta:
    #     model = Idea
    #     fields = ['title','department', 'description', 'image']
    #     labels = {'title':'Title', 'department':'Department', 'description': 'Description', 'image' :'Image'}

    class Meta:
        model = Idea
        fields = ('title', 'description', 'image')

class CriteriaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CriteriaForm, self).__init__(*args, **kwargs)
        self.fields['is_public'].required = False

    notes = forms.CharField(label='Notes', max_length=500, widget=forms.Textarea)
    is_user_led = BooleanField()
    is_public = BooleanField()

    # image = forms.ImageField()
    estimated_cost = forms.DecimalField(required=False)

   
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

    def __init__(self, *args, **kwargs):
        super(ApprovalForm, self).__init__(*args, **kwargs)
        self.fields['startDate'].required = True
        self.fields['endDate'].required = True
        
    def clean_start_date(self):
        date = self.cleaned_data['startDate']
        print(date)
        if date < make_aware(datetime.date.today()):
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    def clean_end_date(self):
        date = self.cleaned_data['endDate']
        if date < make_aware(datetime.date.today()):
            raise forms.ValidationError("The date cannot be in the past!")
        return date            

    class Meta:
        model = Post
        fields = ('startDate', 'endDate', 'status')
        widgets = {
            'startDate': widgets.DateInput(attrs={'type': 'date'}),
            'endDate': widgets.DateInput(attrs={'type': 'date'}),
        }

class IdeaApprovalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(IdeaApprovalForm, self).__init__(*args, **kwargs)
     
    class Meta:
        model = Idea
        fields = ('status',)