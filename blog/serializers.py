# File: forms.py
# Author: Thomas Dion (tdion@bu.edu), 11/13/2026
# Description: Contains the serializers for the dadjokes app
from rest_framework import serializers
from .models import *
 
class ArticleSerializer(serializers.ModelSerializer):
    '''a serializer for the article model'''
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'text', 'published', 'image_file']
    
    # add methods to customize the Create/Read/Update/Delete operations
    def create(self, validated_data):
        '''
        Override the superclass method that handles object creation.
        '''
        print(f'ArticleSerializer.create, validated_data={validated_data}.')
        # create an Article object
        article = Article(**validated_data)
        # attach a FK for the User
        article.user = User.objects.first()
        # save the object to the database
        article.save()
        # return an object instance
        return article
 
 
        # # a simplified way:
        # # attach a FK for the User
        # validated_data['user'] = User.objects.first()
        # # do the create and save all at once
        # return Article.objects.create(**validated_data)