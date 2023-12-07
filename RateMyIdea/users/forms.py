from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import Author
from django.utils.text import slugify

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
		widgets = {
               'image':forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
               }
          

class UpdateAccountDetailsForm(forms.Form):
    """Form for users to change their user details"""
    username = forms.CharField(max_length=255,
                               label="Username (symbols like '#', '.', '/', '!', '@' etc. are not allowed and will be removed automatically)")
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, max_length=2000)

    # updating form to accept request parameters
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UpdateAccountDetailsForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        """username has to be unique"""
        username = self.cleaned_data['username']
        
        # slugify username to remove invalid URL symbols
        slugified_username = slugify(username)

        # is_bound checks if form has received data through a request (typically a POST).
        # check for uniqueness excluding current username
        if self.is_bound and User.objects.filter(username=slugified_username).exclude(pk=self.request.user.pk).exists():
            raise forms.ValidationError("This username is already in use.")
        return slugified_username
     
    def clean_email(self):
        """email has to be unique"""
        email = self.cleaned_data['email']
            
        # check for uniqueness excluding current email
        if self.is_bound and User.objects.filter(email=email).exclude(pk=self.request.user.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email