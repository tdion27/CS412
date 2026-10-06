# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the views for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile, Post

# Create your views here.

#Create the ShowAll view to display all profiles
class ShowAllView(ListView):
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

#Create the Detail view to display a single profile's details
class ProfileView(DetailView):
    model = Profile
    template_name = "mini_insta/profile.html"
    context_object_name = "profile"

#Ctreate the Detail view to display a single post's details
class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"