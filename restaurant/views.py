# File: urls.py
# Author: Thomas Dion (tdion@bu.edu), 9/17/2026
# Description: Contains the views for the restaurant app

from django.shortcuts import render
import random
import time

# Create your views here.

# Link to the image used for the restaurant
image = "https://images.squarespace-cdn.com/content/v1/56d8740586db43f34bc3e823/1466713071671-UB340J4VH2UW48VDMPHU/appgrill_atetrack001.jpg"

# List of specials
specials = [
    "Wild Mushroom Flatbread",
    "Bourbon-Glazed Pork Chop",
    "Shrimp & Grits",
    "Smoked Beef Brisket Sandwich",
    "Lemon-Herb Chicken",
    "BLT Sandwich",
    "Turkey Meatloaf",
    "Catfish Po'Boy",
    "Braised Short Ribs",
]

def main(request):
    '''The homepage of the restaurant'''
    template = "restaurant/main.html"
    context = {
        'image': image,
    }
    return render(request, template, context)


def order(request):
    '''Allow users to create an order'''
    template = "restaurant/order.html"
    context = {
        # Choose a random special for the menu
        'special': random.choice(specials),
    }
    return render(request, template, context)

def submit(request):
    '''Process the order submission, and generate a receipt and total of selected items.'''

    #Set an empty context to avoid passing in null
    context = {}
    template_name = "restaurant/confirmation.html"
    if request.POST:
        #Set customer name from the form
        name = request.POST['name']
        #Set special instructions from the form
        instructions = request.POST['instructions']

        #Initialize variables for list of items and total
        total = 0
        orderItems = []

        #Check for the presence of each item and append it to the list and total, if found in the order
        if 'chicken' in request.POST:
            orderItems.append('Mountain Heritage Fried Chicken')
            total += 15

        if 'roast' in request.POST:
            orderItems.append('Slow-Braised Pot Roast')
            total += 20

        if 'trout' in request.POST:
            orderItems.append('Pan-Seared Trout')
            total += 12

        if 'burger' in request.POST:
            orderItems.append('Burger')
            total += 16

        if 'bacon' in request.POST:
            orderItems.append('Add Bacon')
            total += 7

        if 'veggie' in request.POST:
            orderItems.append('Substitute Veggie Patty')
            total += 2

        if 'special' in request.POST:
            orderItems.append('Special')
            total += 15

        # Pick a random time for the order, add it to the current time, and then format it to be displayed
        random_time = random.uniform(1800, 3600)
        pickup_time = time.time() + random_time
        pickup_time_seconds = time.ctime(pickup_time)

        context = {
            'name': name, 
            'order': orderItems,
            'total': total,
            'pickupTime': pickup_time_seconds,
            'instructions': instructions,
        }

    
    return render(request, template_name=template_name, context=context)