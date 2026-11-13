# File: views.py
# Author: Thomas Dion (tdion@bu.edu), 11/13/2026
# Description: Contains the views for the dadjokes app
import random
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class RandomView(TemplateView):
    '''A view to show one random Joke and one random Picture.'''
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all()) if Joke.objects.exists() else None
        context['picture'] = random.choice(Picture.objects.all()) if Picture.objects.exists() else None
        return context


class JokeListView(ListView):
    ''''A view to show a list of jokes'''
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    '''A view to show one joke and contributer'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    '''A view to show all of the pictures'''
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    '''A view to show the pictures in a list'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


# API views
class RandomJokeAPIView(APIView):
    '''Show one Joke  at random.'''
    def get(self, request):
        joke = random.choice(Joke.objects.all())
        return Response(JokeSerializer(joke).data)


class RandomPictureAPIView(APIView):
    '''Show one Picture  at random.'''
    def get(self, request):
        picture = random.choice(Picture.objects.all())
        return Response(PictureSerializer(picture).data)


class JokeListAPIView(generics.ListCreateAPIView):
    '''Return all Jokes or create a Joke'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''Return a joke'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    '''Return the list of pictures'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''Return a picture's details'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
