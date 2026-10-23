from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

class ShowAllView(ListView):
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"
    
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)

class ArticleView(DetailView):
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

class RandomArticleView(DetailView):
    
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"
    
    def get_object(self):
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article and save it to the database.'''
 
 
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
 
 
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
        
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
        return super().form_valid(form)
        

class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
 
 
        # create and return a URL:
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
 

    def form_valid(self, form):

        
        # instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
            
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK
    
    
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
 
 
        # calling the superclass method
        context = super().get_context_data()
 
 
        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
 
 
        # add this article into the context dictionary:
        context['article'] = article
        return context

class UpdateArticleView(UpdateView):
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        article = comment.artile
        return reverse('article', kwargs={'pk':article.pk})

class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
 
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')