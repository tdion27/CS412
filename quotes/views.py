from django.shortcuts import render
import random

# Create your views here.

quotes = [
"I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.",
"There is no greater agony than bearing an untold story inside you.",
"What you're supposed to do when you don't like a thing is change it. If you can't change it, change the way you think about it. Don't complain.",
]

images = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREhhQIy1oGrPILAcVtdLcMxmvlTnwM5iLrIZP1Ute7-Q&s=10",
    "https://www.zinnedproject.org/wp-content/uploads/2014/05/MayaAngelou-1200x1490.jpg",
    "https://en-chatelaine.mblycdn.com/ench/resized/2014/06/w767/Dr.-Maya-Angelou-in-San-Francisco-1970.jpg",
]

def quote(request):
    template = "quotes/quote.html"
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, template, context)

def show_all(request):
    template = "quotes/show_all.html"
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, template, context)

def about(request):
    template = "quotes/about.html"
    return render(request, template)