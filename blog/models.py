from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    test= models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk' : self.pk})

    def get_all_comments(self):
        comments = Comment.objects.filter(artile=self)
        return comments

class Comment(models.Model):
    artile = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'