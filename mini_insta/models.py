# File: models.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the models  for the mini_insta app
from django.db import models
from django.urls import reverse

# Create your models here.

#Define the Profile Model
class Profile(models.Model):
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    #Allow a string representation for a profile to be created
    def __str__(self):
        return f'{self.username}'

    def get_all_posts(self):
            posts = Post.objects.filter(profile=self)
            return posts

#Define the Post model
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    #Allow a string representation for a post to be created
    def __str__(self):
            return f'{self.caption}'

    #Get method for photos
    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    #Create the URL for for submission
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
#Define the Photo model
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    #Allow a string representation for a photo to be created
    def __str__(self):
        if self.image_url:
            return f'{self.image_url}'
        elif self.image_file:
             return f'{self.image_file.url}'
        return f'Photo {self.pk}'

    #Get method image URL
    def get_image_url(self):
         if self.image_url:
              return self.image_url
         elif self.image_file:
              return self.image_file.url
         return None