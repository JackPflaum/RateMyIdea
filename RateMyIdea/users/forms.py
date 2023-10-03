from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import Author

class SignUpForm(UserCreationForm):
    """User signup form"""

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2',)

    def clean_email(self):
        """validate and clean email data"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address has already been taken")
        return email
        
    def clean_username(self):
        """validate and clean username data"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username has already been taken")
        return username

    def save(self, commit=True):
        """save user data to the User database"""
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
        return user
        

class UserChangeForm(UserChangeForm):
    """form for users to change their user details"""
    class Meta:
        models = User
        fields = ('username', 'email',)


class UpdateImageForm(forms.ModelForm):
	"""Form for users to change their profile image"""
	class Meta:
		model = Author
		fields = ['image']
		widgets = {'image':forms.ClearableFileInput(attrs={'class': 'form-control-file'}),}