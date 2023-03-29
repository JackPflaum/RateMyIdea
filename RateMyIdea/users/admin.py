from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Author

# using custom user model, therefore have to define new admin class that inherits UserAdmin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Author)