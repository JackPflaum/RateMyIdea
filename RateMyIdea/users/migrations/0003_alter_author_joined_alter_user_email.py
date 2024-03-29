# Generated by Django 4.1.7 on 2023-09-14 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_author_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='joined',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
