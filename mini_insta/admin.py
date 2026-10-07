# File: models.py
# Author: Thomas Dion (tdion@bu.edu)
# Description: Registers the models for the mini_insta app
from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Photo

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)