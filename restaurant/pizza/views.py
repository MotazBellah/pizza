from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Type, Size, Topping, Order, Menu, Purchase, Product
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import stripe

import sendgrid
import os
from sendgrid.helpers.mail import *

xxxx = os.environ.get('FACEBOOK_KEY')  # App ID
yyyy =os.environ.get('SENDGRID_KEY') #app key

def send_email_SendGrid(user_email, message):
    print('//////////////////////////////////')
    print(os.environ.get('SENDGRID_KEY'))
    print('//////////////////////////////////')
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
    data = {
      "personalizations": [
        {
          "to": [
            {
              "email": "{}".format(user_email)
            }
          ],
          "subject": "Hello from the Pizza Online Order!"
        }
      ],
      "from": {
        "email": "moataz.ghobashi@gmail.com"
      },
      "content": [
        {
          "type": "text/plain",
          "value": "{}".format(message)
        }
      ]
    }
    response = sg.client.mail.send.post(request_body=data)


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})


    products = Product.objects.all()
    category = Type.objects.all()
    if request.method == "POST":
        food = request.POST['name']
        price = request.POST['price']
        print(food, price)
        item_type = Type.objects.get(name='Popular')
        print('//////////////////')
        print(item_type)
        cart = Order(item=food, user=request.user, price=price, type=item_type)
        cart.save()
        return HttpResponseRedirect(reverse("index"))

    context = {
        'category': category,
        'products': products
    }
    # return render(request, "pizza/index.html", context)
    return render(request, "pizza/index2.html", context)

def menus(request, item_id):
    items = Menu.objects.filter(type=item_id)
    print(items)
    food = [Size.objects.filter(menu=i) for i in items]
    print(food)
    category = Type.objects.all()
    # for i in food:
    #     print(i[0])
    # print(food)
    context = {
        'food': [i[0] for i in food],
        'toppings': Topping.objects.all(),
        'category': category,
        'item_id': item_id,
    }
        # return render(request, "pizza/index.html", context)
    return render(request, "pizza/menu.html", context)


def addFood(request):
    x = request.POST["food"]
    y = request.POST.getlist("add1")
    z = request.POST.getlist("add2")
    type = request.POST["id"]
    topping_list = request.POST.getlist("topping1")

    item_type = Type.objects.get(pk=type)

    add_ons = ['+ Mushrooms', '+ Green Peppers', '+ Onions', 'Extra Cheese on any sub']
    if x in add_ons:
        items = Order.objects.filter(type=item_type, user=request.user)
        subs = [i.item for i in items if i.item not in add_ons]
        for add in add_ons:
            if x == add:
                extra_add = [i.item for i in items if i.item == add]
                if len(subs) <= len(extra_add):
                    print("TEST")
                    return HttpResponseRedirect(reverse("index"))


    print(item_type)
    print(z)
    print(topping_list)
    # print(topping2)
    # print(topping3)
    if y:
        price = y[0]
    else:
        price = z[0]


    if x in ['1 topping', '1 item', '2 toppings', '2 items', '3 toppings', '3 items', 'Special']:
        # y = x +" (" +", ".join(topping_list) +')'
        cart = Order(item=x, user=request.user, price=price, type=item_type)
        cart.save()
        for t in topping_list[0].split(','):
            a = Topping.objects.get(item=t)
            cart.topping.add(a)
    else:
        cart = Order(item=x, user=request.user, price=price, type=item_type)
        cart.save()

    return HttpResponseRedirect(reverse("index"))


def carts(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    print("***********************************request.user.email******************************")
    print(request.user.email)
    print(request.user)
    print("***********************************request.user.email******************************")
    # food = [([i.item, i.price], i.id, i.type) for i in shopping]
    # for i in shopping:
    #     for topping in i.topping.all():
    #         print(topping)
    #     print(i.type)
    #     print(i.topping)

    context = {
        'food': shopping,
        'price': round(total_price, 2),

    }
    return render(request, "pizza/payment.html", context)

def payments(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})

    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    email_message = 'Please find your order below: \n\n'

    if request.method == "POST":
        print(request.user.email)
        token = request.POST.get('token', False)
        print(token)

        pay = stripe.Charge.create(
              amount=int(round(total_price, 2) * 100),
              currency="usd",
              source=token,
              description=request.user.email,
        )

        for i in shopping:
            Purchase(order=i.item, user=request.user, price=i.price).save()
            email_message += i.item + "  " + str(i.price) + '\n'

        email_message += 'Total price is {}'.format(str(total_price))
        Order.objects.filter(user=request.user).delete()
    # print(email_message)

        try:
            send_email_SendGrid(request.user.email, email_message)
        except Exception as e:
            print(e)
            pass

        return HttpResponseRedirect(reverse("carts"))


def delete(request, item_id):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    delete_order = Order.objects.get(pk=item_id)
    delete_order.delete()

    type = Type.objects.get(name='Subs')
    get_subs = Order.objects.filter(type=type.id, user=request.user)

    add_ons = ['+ Mushrooms', '+ Green Peppers', '+ Onions', 'Extra Cheese on any sub']
    items_name = [i.item for i in get_subs if i.item not in add_ons]
    extra_exsit = [i.item for i in get_subs if i.item in add_ons]

    if extra_exsit and not items_name:
        for i in extra_exsit:
            print(i)
            Order.objects.filter(item=i, user=request.user).delete()

    return HttpResponseRedirect(reverse("carts"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if not password == password2:
            return render(request, "pizza/register.html", {"message":"Passwords don't match."})

        user = User.objects.create_user(username, email, password)
        user.username = username
        user.email = email
        user.save()

        return render(request, "pizza/login.html", {"message":"Registered. You can log in now."})
    return render(request, "pizza/register.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "pizza/login.html", {"message": "Invalid credentials."})
    return render(request, "pizza/login.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "pizza/login.html", {"message": "Logged out."})
