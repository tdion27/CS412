# File: urls.py
# Author: Thomas Dion (tdion@bu.edu), 9/29/2026
# Description: Contains the url paths for the mini_insta app

from django.urls import path
from .views import ShowAllView, ProfileView
 
# define the url patterns for the application
urlpatterns = [       
    path('', ShowAllView.as_view(), name='show_all'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile')
]
