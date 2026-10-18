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
        '''create a string representation of a post'''
        return f'{self.username}'

    def get_all_posts(self):
            '''get method for all posts associated with a profile'''
            posts = Post.objects.filter(profile=self)
            return posts
    
    def get_followers(self):
        '''Get the followers for a profile'''
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        '''Count the number of followers of a profile'''
        return len(self.get_followers())

    def get_following(self):
        '''Get the profiles a user is following'''
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
         '''Get the number of profiles a user is following'''
         return len(self.get_following())

    def get_post_feed(self):
         '''Get only the posts created by profiles that the user is following'''
         following_profiles = self.get_following()
         return Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')

#Define the Post model
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    #Allow a string representation for a post to be created
    def __str__(self):
            '''create a string representation of the post'''
            return f'{self.caption}'

    #Get method for photos
    def get_all_photos(self):
        '''get method for photos'''
        photos = Photo.objects.filter(post=self)
        return photos

    #Create the URL for for submission
    def get_absolute_url(self):
        '''get success URL upon form submission'''
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_all_comments(self):
        '''Get the comments for the specific post'''
        return Comment.objects.filter(post=self).order_by('timestamp')

    def get_likes(self):
        '''Get the likes for a specific post'''
        return Like.objects.filter(post=self)
    
#Define the Photo model
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    #Allow a string representation for a photo to be created
    def __str__(self):
        '''create a string representation of the photo'''
        if self.image_url:
            return f'{self.image_url}'
        elif self.image_file:
             return f'{self.image_file.url}'
        return f'Photo {self.pk}'

    #Get method image URL
    def get_image_url(self):
         '''get the image URL'''
         if self.image_url:
              return self.image_url
         elif self.image_file:
              return self.image_file.url
         return None

#Define the follow model
class Follow(models.Model):

     #Use relared_name because we have two foreign keys
     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
     follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
     time_of_follow = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        '''Creates a string representation for a follow relationship'''
        return f"{self.follower_profile.username} follows {self.profile.username}"

#Define the Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''The string represntation of a comment'''
        return f"{self.profile.username} commented on Post {self.post.pk}"

#Define the Like model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Creates a string representation of a like'''
        return f"{self.profile.username} liked Post {self.post.pk}"