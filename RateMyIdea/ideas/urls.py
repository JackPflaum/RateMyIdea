from django.urls import path
from . import views
from .views import IdeaView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ideas'

urlpatterns = [
    path('', views.home, name='home'),
    path('idea/<slug:slug>', IdeaView.as_view(), name='idea'),
    path('new_idea/', views.new_idea, name='new_idea'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('author/<slug:slug>', views.author, name='author'),
    path('author/edit_profile/<slug:slug>', views.edit_profile, name='edit_profile'),
    path('update_profile_image/<int:user_id>', views.update_profile_image, name='update_profile_image'),
    path('author/about/<slug:slug>', views.about_author, name='about_author'),
    path('author/security/<slug:slug>', views.profile_security, name='profile_security'),
    path('author/delete_account/', views.delete_account, name='delete_account'),
    path('author/delete_idea/<slug:idea_slug>/<slug:author_slug>/', views.delete_idea, name='delete_idea'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # serves uploaded media files during development