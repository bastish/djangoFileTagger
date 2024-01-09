from django import forms
from .models import AccessibleDirectory

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = AccessibleDirectory
        fields = ['path']
