from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Idea(models.Model):
    title = models.CharField(max_length=255, unique=True)
    idea = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='idea_authored')
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + ' ' + self.author.username)
            super().save(*args, **kwargs)


    def __str__(self):
        return f'Idea: {self.title} by {self.author.username}'
    

class Rating(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='idea_rating')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors_rating')
    rating = models.DecimalField(max_digits=3, decimal_places=1)


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='idea_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors_comment')
    comment = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
