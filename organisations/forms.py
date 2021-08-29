from django import forms
from .models import Organisation

class OrgForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ('name',)