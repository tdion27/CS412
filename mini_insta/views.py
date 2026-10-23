# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the views for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Like, Follow
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

#Create a LogIn MixIn with custom properties 
class CustomLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        '''create the url for the page displayed when a user logs out'''
        return reverse('login')
    
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
class CreatePostView(CreateView, CustomLoginRequiredMixin):
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    #Get context items for the post form
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    #Method to attach Profile and process images
    def form_valid(self, form):
        '''Overwrite form_valid method to attach foreign key'''
        profile = Profile.objects.get(user=self.request.user)
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
        return reverse('profile')
    
    def get_object(self):
        # Finds the profile associated with the currently logged-in user
        return Profile.objects.get(user=self.request.user)

#Create the update view to update a post
class UpdatePostView(UpdateView, CustomLoginRequiredMixin):
    model = Post
    template_name = "mini_insta/update_post_form.html"
    fields = ['caption']

    def get_context_data(self, **kwargs):
        '''Override the default method to attach the corresponding profile to the post'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_success_url(self):
            '''Create the success url on successful submission of the form'''
            pk = self.kwargs['pk']
            return reverse('post_detail', kwargs={'pk': pk})

#Create the delete view to delete a post
class DeletePostView(DeleteView, CustomLoginRequiredMixin):
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        '''Attaches the corresponding profile to the context data'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        '''Create the URL for redirection upon submission of the form'''
        return reverse('profile')

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
class ShowFeedView(DetailView, CustomLoginRequiredMixin):
     model = Profile
     template_name = "mini_insta/show_feed.html"
     context_object_name = "profile"

     def get_object(self):
        '''Get the profile associated with the logged in user'''
        return Profile.objects.get(user=self.request.user)

#Create the list view to allow searching Mini Insta
class SearchView(ListView):
    template_name = 'mini_insta/search_results.html'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the default dispatch method to check for the presence of a query'''
        query = self.request.GET.get('query')
        if not query: #Show the search form
            profile = Profile.objects.get(user=self.request.user)
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
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['query'] = query
        context['posts'] = self.get_queryset()

        #Ensure that the profile can be found based on bio, display name, or username
        context['profiles'] = (
            Profile.objects.filter(username__icontains=query) |
            Profile.objects.filter(display_name__icontains=query) |
            Profile.objects.filter(bio_text__icontains=query)
        )
        return context

#Define the profile view when a user is logged in 
class LoggedInProfileView(CustomLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_insta/profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get the profile associated with the logged in user'''
        return Profile.objects.get(user=self.request.user)

#Define the logout view
class LogoutConfirmationView(TemplateView):
    template_name = 'mini_insta/logged_out.html'

#Define the view to create a user/profile
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''Create the context for the template'''
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Override the super form_valid method to use both forms'''
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        '''Create the url to redirect to upon successful submission'''
        return reverse('profile')

#Define the view to allow follows
class FollowView(CustomLoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/profile.html'
    context_object_name = 'profile'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the super dispatch method'''
        target_profile = Profile.objects.get(pk=kwargs['pk'])
        logged_in_profile = Profile.objects.get(user=request.user)
        Follow.objects.get_or_create(profile=target_profile, follower_profile=logged_in_profile) 
        return super().dispatch(request, *args, **kwargs)

#Define the view to allow unfollows
class UnfollowView(CustomLoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/profile.html'
    context_object_name = 'profile'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the super dispatch method'''
        target_profile = Profile.objects.get(pk=kwargs['pk'])
        logged_in_profile = Profile.objects.get(user=request.user)
        Follow.objects.filter(profile=target_profile, follower_profile=logged_in_profile).delete()
        return super().dispatch(request, *args, **kwargs)

#Define the view to allow a user to like posts 
class LikeView(CustomLoginRequiredMixin, DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the super dispatch method'''
        post = Post.objects.get(pk=kwargs['pk'])
        logged_in_profile = Profile.objects.get(user=request.user)
        Like.objects.get_or_create(post=post, profile=logged_in_profile)
        return super().dispatch(request, *args, **kwargs)

#Define the view to allow a user to unlike a post
class UnlikeView(CustomLoginRequiredMixin, DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the super dispatch method'''
        post = Post.objects.get(pk=kwargs['pk'])
        logged_in_profile = Profile.objects.get(user=request.user)
        Like.objects.filter(post=post, profile=logged_in_profile).delete()
        return super().dispatch(request, *args, **kwargs)