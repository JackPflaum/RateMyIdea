from django.urls import path
from . import views

app_name = 'ideas'

urlpatterns = [
    path('', views.home, name='home'),
    path('idea/<slug:slug>', views.idea, name='idea'),
    path('new_idea/', views.new_idea, name='new_idea'),
    path('author/<slug:slug>', views.author, name='author'),
]
