from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Idea
from .forms import NewIdeaForm
from django.contrib.auth.decorators import login_required

def home(request):
    ideas_list = Idea.objects.all()

    # ideas per page from Idea model
    paginator = Paginator(ideas_list, 20)

    # retrieve page number
    page = request.GET.get('page')
    ideas = paginator.get_page(page)
    context = {'ideas': ideas}
    return render(request, 'home.html', context)


def idea(request, slug):
    pass


@login_required
def new_idea(request):
    """new idea form for users to write their idea"""
    if request.method == 'POST':
        form = NewIdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewIdeaForm()
    return render(request, 'new_idea.html', {'form': form})


def author(request, slug):
    pass