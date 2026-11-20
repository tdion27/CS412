# File: serializers.py
# Author: Thomas Dion (tdion@bu.edu), 11/19/2026
# Description: Contains the serializers for the mini_insta REST API
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class PhotoSerializer(serializers.ModelSerializer):
    '''A serializer for the Photo model.'''
    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'image_file', 'timestamp']


class PostSerializer(serializers.ModelSerializer):
    '''A serializer for reading Posts'''
    photos = PhotoSerializer(many=True, read_only=True, source='get_all_photos')
    profile_username = serializers.CharField(source='profile.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'profile_username', 'caption', 'timestamp', 'photos']
        read_only_fields = ['profile']


class CreatePostSerializer(serializers.ModelSerializer):
    '''A serializer for creating a Post with an image'''
    image_url = serializers.URLField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Post
        exclude = ['profile']

    def create(self, validated_data):
        '''Create the post, and an optional photo'''
        image_url = validated_data.pop('image_url', '')
        post = Post.objects.create(**validated_data)
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)
        return post

    def to_representation(self, instance):
        return PostSerializer(instance, context=self.context).data


class ProfileSerializer(serializers.ModelSerializer):
    '''A serializer for Profile model'''
    num_posts = serializers.SerializerMethodField()
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date', 'num_posts', 'num_followers', 'num_following']

    def get_num_posts(self, obj):
        return obj.get_all_posts().count()

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()


class UserSerializer(serializers.ModelSerializer):
    '''A serializer for creating a user'''
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        '''A method to create a user with a profile'''
        user = User.objects.create_user( username=validated_data['username'], password=validated_data['password'], email=validated_data.get('email'))
        Profile.objects.create(user=user, username=user.username, display_name=user.username)
        return user
