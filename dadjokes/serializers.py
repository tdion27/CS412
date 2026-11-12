from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    '''A serializer for the Joke model.'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    '''A serializer for the Picture model.'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']
