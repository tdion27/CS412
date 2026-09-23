from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.conf import settings
 
 
urlpatterns = [ 
    path(r'', views.main, name="main"),          
    path('order/', views.order, name="order"),
    path('confirmation/', views.submit, name="confirmation"),
]