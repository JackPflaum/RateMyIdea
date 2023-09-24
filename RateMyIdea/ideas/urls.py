from django.urls import path
from . import views
from .views import IdeaView

app_name = 'ideas'

urlpatterns = [
    path('', views.home, name='home'),
    path('idea/<slug:slug>', IdeaView.as_view(), name='idea'),
    path('new_idea/', views.new_idea, name='new_idea'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('author/<slug:slug>', views.author, name='author'),
    path('author/edit_profile/<slug:slug>', views.edit_profile, name='edit_profile'),
    path('author/security/<slug:slug>', views.profile_security, name='profile_security'),
    path('author/delete_account', views.delete_account, name='delete_account'),
    path('author/delete_idea/<slug:idea_slug>/<slug:author_slug>/', views.delete_idea, name='delete_idea'),
]
