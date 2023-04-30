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

    # we need to pass the existing instance to the form argument if it does exist.
    # '__init__' modifies the form behaviour so that it prepopulates the rating field in the form.
    # the '__init__' method gets called when you create a new instance of the form.
    
    # def __init__(self, *args, **kwargs):
    #     # pass existing rating to the form
    #     super().__init__(*args, **kwargs)    # call parent class first to ensure form is properly initialized.
    #     self.instance = kwargs.get('instance')    # check if an instance parameter is provided in kwargs.

    #     # create a new dictionary which holds initial values for the form field.
    #     # it checks if there are existing initial values in kwargs dict.
    #     # if there are initial values, it copies them into 'initial' value.
    #     # if there are no existing initial values, it sets initial to an empty dict.
    #     initial = kwargs.get('initial', {})

    #     # set existing instance rating value to the rating field or set to None if one doesn't exist.
    #     initial['rating'] = self.instance.rating if self.instance else None
    #     kwargs['initial'] = initial

    class Meta:
        model = Rating
        fields = ('rating',)
        widgets = {'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 11)])}