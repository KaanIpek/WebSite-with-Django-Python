from django import forms
from .models import Job
class JobForm(forms.ModelForm):
    class Meta:
        model= Job
        fields=["title","district","email","telno","location","fee","content"]

