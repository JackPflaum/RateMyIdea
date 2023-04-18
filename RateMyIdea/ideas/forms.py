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

    # the default behaviour of modelForm is to create a new instance if one doesn't exist.
    # we need to pass the existing instance to the form argument.
    # '__init__' modifies the form behaviour so that it prepopulates the rating field in the form.

    def __init__(self, *args, **kwargs):
        # Pass the existing rating value to the form
        self.instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        initial['rating'] = self.instance.rating if self.instance else None
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = Rating
        fields = ['rating']

    class Meta:
        model = Rating
        fields = ('rating',)
        widgets = {'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 11)])}