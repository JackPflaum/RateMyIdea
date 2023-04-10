from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Author, User


@receiver(post_save, sender=User)
def create_author_model(sender, instance, created, **kwargs):
    """create a Author instance for the User that was created"""
    if created:
        Author.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_author_profile(sender, instance, **kwargs):
    """save Author instance"""
    instance.author.save()