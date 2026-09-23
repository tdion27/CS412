# File: urls.py
# Author: Thomas Dion (tdion@bu.edu), 9/17/2026
# Description: Contains the url paths for the restaurant app

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.conf import settings
 
# define the url patterns for the application
urlpatterns = [ 
    path(r'', views.main, name="main"),          
    path('order/', views.order, name="order"),
    path('confirmation/', views.submit, name="confirmation"),
]
