# File: urls.py
# Author: Thomas Dion (tdion@bu.edu), 11/13/2026
# Description: Contains the urls for the dadjokes app
from django.urls import path
from .views import *

#Define the URL patterns here:
urlpatterns = [
    path('', RandomView.as_view(), name='dadjokes_home'),
    path('random', RandomView.as_view(), name='dadjokes_random'),
    path('jokes', JokeListView.as_view(), name='dadjokes_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='dadjokes_joke'),
    path('pictures', PictureListView.as_view(), name='dadjokes_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='dadjokes_picture'),
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),
    path('api/jokes', JokeListAPIView.as_view()),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view()),
    path('api/pictures', PictureListAPIView.as_view()),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view()),
    path('api/random_picture', RandomPictureAPIView.as_view()),
]
