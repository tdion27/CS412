# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the views for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
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
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    #Method to attach Profile and process images
    def form_valid(self, form):
        '''Overwrite form_valid method to attach foreign key'''
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

#Create the Update View to update a Profile
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_success_url(self):
        '''Create the success URL upon submission of the update form'''
        pk = self.kwargs['pk']
        return reverse('profile', kwargs={'pk':pk})

#Create the update view to update a post
class UpdatePostView(UpdateView):
    model = Post
    template_name = "mini_insta/update_post_form.html"
    fields = ['caption']

    def get_context_data(self, **kwargs):
        '''Override the default method to attach the corresponding profile to the post'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
            '''Create the success url on successful submission of the form'''
            pk = self.kwargs['pk']
            return reverse('post_detail', kwargs={'pk': pk})

#Create the delete view to delete a post
class DeletePostView(DeleteView):
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        '''Attaches the corresponding profile to the context data'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        '''Create the URL for redirection upon submission of the form'''
        pk = self.object.profile.pk
        return reverse('profile', kwargs={'pk':pk})

#Create the detail view to show the followers of a profile
class ShowFollowersDetailView(DetailView):
     model = Profile
     template_name = 'mini_insta/show_followers.html'
     context_object_name = 'profile'

#Create the detail view to show the profiles a user is following
class ShowFollowingDetailView(DetailView):
     model = Profile
     template_name = 'mini_insta/show_following.html'
     context_object_name = 'profile'

#Create the detail view to show a profile's feed
class ShowFeedView(DetailView):
     model = Profile
     template_name = "mini_insta/show_feed.html"
     context_object_name = "profile"

#Create the list view to allow searching Mini Insta
class SearchView(ListView):
    template_name = 'mini_insta/search_results.html'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the default dispatch method to check for the presence of a query'''
        query = self.request.GET.get('query')
        if not query: #Show the search form
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Filter the posts and profiles based on the search query'''
        query = self.request.GET.get('query')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        '''Create necessary context variables for the template'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query') 
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        context['query'] = query
        context['posts'] = self.get_queryset()

        #Ensure that the profile can be found based on bio, display name, or username
        context['profiles'] = (
            Profile.objects.filter(username__icontains=query) |
            Profile.objects.filter(display_name__icontains=query) |
            Profile.objects.filter(bio_text__icontains=query)
        )
        return context

