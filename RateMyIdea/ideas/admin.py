from django.contrib import admin
from .models import Idea, Rating


# customize how the models are displayed in the admin interface
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'idea', 'author', 'date_posted', 'date_modified', 'slug')


class RatingAdmin(admin.ModelAdmin):
    list_display = ('idea', 'author', 'rating')


# Register your models here.
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Rating, RatingAdmin)