# Generated by Django 4.1.7 on 2023-10-03 10:16

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_author_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, default='images/default_profile_image.png', upload_to=users.models.user_image_upload_destination),
        ),
    ]