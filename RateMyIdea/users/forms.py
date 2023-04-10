from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import Author

class SignUpForm(UserCreationForm):
    """User signup form"""

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2',)

        def save(self, commit=True):
            """clean email data and save user email to the User"""
            user = super(SignUpForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
        

class UserChangeForm(UserChangeForm):
    """form for users to change their user details"""
    class Meta:
        models = User
        fields = ('username', 'email',)