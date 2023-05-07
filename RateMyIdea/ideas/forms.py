from django import forms
from .models import Idea, Comment, Rating

class NewIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title','idea')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('rating',)
        widgets = {'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 11)])}