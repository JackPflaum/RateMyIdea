from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from users.models import User


def signup(request):
    """user signup form and authentication"""
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()    # save the form data to the database
        email = form.cleaned_data['email']    # email data cleaned in SignUpForm method clean_email
        password = form.cleaned_data.get('password1')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signup successful', extra_tags='alert-success')
            return redirect('ideas:home')
    return render(request, 'signup.html', {'form': form})
