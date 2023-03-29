from django import forms
from .models import Idea

class NewIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title','idea')