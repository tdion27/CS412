# File: models.py
# Author: Thomas Dion (tdion@bu.edu), 11/13/2026
# Description: Contains the models for the dadjokes app
from django.db import models


class Joke(models.Model):
    '''A model to define a joke'''
    text = models.TextField(blank=False)
    name = models.CharField(max_length=100, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.text} - {self.name}'


class Picture(models.Model):
    '''A model to define a photo'''
    image_url = models.URLField(blank=False)
    name = models.CharField(max_length=100, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.image_url} - {self.name}'
