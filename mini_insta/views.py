# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the views for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
from django.urls import reverse

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

#Create the Detail view to display a single post's details
class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

#Create the Create view to create a post
class CreatePostView(CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    #Get context items for the post form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    #Method to attach Profile and process images
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])    
        form.instance.profile = profile
        response = super().form_valid(form)

        #Commenting out old code
        #image_url = self.request.POST.get('image_url')
        #if image_url:
        #    Photo.objects.create(post=self.object, image_url=image_url) 
        
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)
        return response