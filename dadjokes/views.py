import random
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class RandomView(TemplateView):
    '''Show one random Joke and one random Picture.'''
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all()) if Joke.objects.exists() else None
        context['picture'] = random.choice(Picture.objects.all()) if Picture.objects.exists() else None
        return context


class JokeListView(ListView):
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'


# REST API:

class RandomJokeAPIView(APIView):
    '''Return one Joke selected at random.'''
    def get(self, request):
        joke = random.choice(Joke.objects.all())
        return Response(JokeSerializer(joke).data)


class RandomPictureAPIView(APIView):
    '''Return one Picture selected at random.'''
    def get(self, request):
        picture = random.choice(Picture.objects.all())
        return Response(PictureSerializer(picture).data)


class JokeListAPIView(generics.ListCreateAPIView):
    '''Return all Jokes (GET) or create a Joke (POST).'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
