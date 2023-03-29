from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('idea/<slug:slug>', views.idea, name='idea'),
    path('new_idea/', views.new_idea, name='new_idea'),
    path('author/<slug:slug>', views.author, name='author'),
]
