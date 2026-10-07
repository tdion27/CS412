# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 10/7/2026
# Description: Contains the forms for the mini_insta app
from django import forms
from.models import *

#Define the form and fields to create a post 
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']
