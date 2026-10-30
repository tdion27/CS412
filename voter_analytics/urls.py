# File: urls.py
# Author: Thomas Dion (tdion@bu.edu), 10/27/2026
# Description: Contains the urls for the voter_analytics app

from django.urls import path
from . import views

#Define the URL paths for the application
urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.VoterGraphsView.as_view(), name='graphs'),
]