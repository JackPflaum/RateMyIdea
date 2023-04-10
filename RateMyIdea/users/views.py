from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate



def signup(request):
    """user signup form and authentication"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()    # save the form data to the database
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

