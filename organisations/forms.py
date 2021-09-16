from django import forms
from .models import Organisation

class OrgForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ('name',)

# class CustomForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(CustomForm, self).__init__(*args, **kwargs)
    #     self.fields['department'].queryset = Department.objects.filter(is_approved=True)
    #     self.fields['additional_field'].required = False
    #     self.fields['image'].required = False

    # class Meta:
    #     model = OrgForm
    #     fields = ['title','department', 'description', 'severity', 'additional_field', 'image',]
    #     labels = {'title':'Title', 'department':'Department', 'description': 'Description', 'severity': 'Severity', 'additional_field': 'Extra', 'image':'Add an attachment',}
