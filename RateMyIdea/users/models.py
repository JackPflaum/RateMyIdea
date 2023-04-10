from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        """create and save a user with the submitted email and password"""
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """create and save a superuser with the submitted email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuse=True')
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model"""
    # in settings.py add AUTH_USER_MODEL = '<appname>.<custom_user_model_class>'

    email = models.EmailField(_('email_address'), unique=True)

    objects = UserManager()

    # email is now used instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Author(models.Model):
    """This model represents the users profile"""
    # extending User model using one-to-one link and signals in signals.py
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    bio = models.TextField()
    image = models.ImageField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
