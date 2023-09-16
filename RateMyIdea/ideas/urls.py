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
    path('author/update_profile/<slug:slug>', views.update_profile, name='update_profile'),
]
