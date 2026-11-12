from django.db import models


class Joke(models.Model):
    '''Encapsulate the data for a joke.'''
    text = models.TextField(blank=False)
    name = models.CharField(max_length=100, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.text} - {self.name}'


class Picture(models.Model):
    '''Encapsulate the data for a silly picture or GIF.'''
    image_url = models.URLField(blank=False)
    name = models.CharField(max_length=100, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.image_url} - {self.name}'
