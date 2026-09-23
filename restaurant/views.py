from django.shortcuts import render
import random
import time

# Create your views here.
image = "https://images.squarespace-cdn.com/content/v1/56d8740586db43f34bc3e823/1466713071671-UB340J4VH2UW48VDMPHU/appgrill_atetrack001.jpg"

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
    template = "restaurant/main.html"
    context = {
        'image': image,
    }
    return render(request, template, context)


def order(request):
    template = "restaurant/order.html"
    context = {
        'special': random.choice(specials),
    }
    return render(request, template, context)

def submit(request):
    '''Process the form submission, and generate a result.'''
 
    context = {}
    template_name = "restaurant/confirmation.html"
    if request.POST:
        name = request.POST['name'] 

        total = 0
        orderItems = []

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

        random_time = random.uniform(1800, 3600)
        pickup_time = time.time() + random_time
        pickup_time_seconds = time.ctime(pickup_time)

        context = {
            'name': name, 
            'order': orderItems,
            'total': total,
            'pickupTime': pickup_time_seconds,
        }

    
    return render(request, template_name=template_name, context=context)