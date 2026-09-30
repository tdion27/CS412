# File: models.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the models  for the mini_insta app
from django.db import models

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