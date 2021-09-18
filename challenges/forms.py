from django import forms
from django.db.models import fields
from django.forms import  widgets
from django.contrib.auth import get_user_model
from django.forms.fields import BooleanField
from .models import Idea, Challenge, Department, IdeaComment, OrgForm
from blog.models import Post
import datetime
from django.utils.timezone import make_aware

class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('title', 'description', 'image', 'is_pridar')
        labels = {'is_pridar': 'Technology-related?'}

class OrgSpecificForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(OrgSpecificForm, self).__init__(*args, **kwargs)
        self.fields['is_public'].required = False

    notes = forms.CharField(label='Notes', max_length=500, widget=forms.Textarea)
    is_user_led = BooleanField()
    is_public = BooleanField()
    estimated_cost = forms.DecimalField(required=False)
    field_1 = BooleanField()
    field_2= BooleanField()
    field_3 = BooleanField()
    field_4 = BooleanField()
    field_5 = BooleanField()
    field_6 = BooleanField()
    field_7 = BooleanField()
    field_8 = BooleanField()
    field_9 = BooleanField()
    field_10 = BooleanField()
    field_11 = BooleanField()
    field_12 = BooleanField()
    field_13 = BooleanField()
    field_14 = BooleanField()
    field_15 = BooleanField()
    field_16 = BooleanField()
    field_17 = BooleanField()
    field_1_name = forms.CharField(label='Notes', max_length=100)
    field_2_name= forms.CharField(label='Notes', max_length=100)
    field_3_name = forms.CharField(label='Notes', max_length=100)
    field_4_name = forms.CharField(label='Notes', max_length=100)
    field_5_name = forms.CharField(label='Notes', max_length=100)
    field_6_name = forms.CharField(label='Notes', max_length=100)
    field_7_name = forms.CharField(label='Notes', max_length=100)
    field_8_name = forms.CharField(label='Notes', max_length=100)
    field_9_name = forms.CharField(label='Notes', max_length=100)
    field_10_name = forms.CharField(label='Notes', max_length=100)
    field_11_name = forms.CharField(label='Notes', max_length=100)
    field_12_name = forms.CharField(label='Notes', max_length=100)
    field_13_name = forms.CharField(label='Notes', max_length=100)
    field_14_name = forms.CharField(label='Notes', max_length=100)
    field_15_name = forms.CharField(label='Notes', max_length=100)
    field_16_name = forms.CharField(label='Notes', max_length=100)
    field_17_name = forms.CharField(label='Notes', max_length=100)

class PRIDARForm(forms.ModelForm):
    class Meta:
        model = OrgForm
        # fields = '__all__'
        fields = ['estimated_cost', 'notes', 'is_user_led', 'in_sandbox', 'is_released_and_supported','is_open_source_partnership','NICE_Tier1_DTAC_evidence_in_place','NICE_Tier2_DTAC_evidence_in_place','risk_and_mitigations_are_public','ce_mark_dcb_register','safety_officer_stated','iso_supplier','user_kpis_is_an_ai_pathway_are_defined','user_to_board_approval_obtained','cost_of_dev_and_support_agreed','ip_agreement_in_place','ig_agreements_in_place','data_and_model_agreed',]
        labels = {'estimated_cost':'Estimated cost?', 'notes':'Notes', 'is_user_led':'Is user led?','in_sandbox':'Is in sandbox?','is_released_and_supported':'Is released and supported?','is_open_source_partnership':'Is an open source partnership?','NICE_Tier1_DTAC_evidence_in_place':'Has nice Tier 1+ DTAC evidence in place','NICE_Tier2_DTAC_evidence_in_place':'Has NICE Tier 2+ DTAC evidence in place','risk_and_mitigations_are_public':'Risks and mitigations are public?','ce_mark_dcb_register':'CE mark/DCB register?','ISO supplier':'ISO supplier?','safety_officer_stated':'Is safety officer stated?','user_kpis_is_an_ai_pathway_are_defined':'User KPIs in an AI Pathway are defined?','user_to_board_approval_obtained':'User to board approval obtained?','cost_of_dev_and_support_agreed':'Cost of dev and support agreed?','ip_agreement_in_place':'IP agreement in place?','ig_agreements_in_place':'IG agreements in place?','data_and_model_agreed':'Data and model is agreed?',}



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

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_approved=True)
        self.fields['sub_department'].required = False

class ChallengeForm(forms.ModelForm):

    additional_field = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.filter(is_approved=True)
        self.fields['additional_field'].required = False
        self.fields['image'].required = False

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