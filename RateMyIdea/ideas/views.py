from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Idea

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


def new_idea(request):
    pass


def author(request, slug):
    pass