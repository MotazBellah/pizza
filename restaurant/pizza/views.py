from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Type, Size, Topping, Order, Menu, Purchase
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    # context = {
    #     'items': [str(i).split(', ') for i in Size.objects.all()]
    # }
    # items = [str(i).split(', ') for i in Size.objects.all()]
    items = [(str(i) + ", " + str(i.id)).split(', ')for i in Size.objects.all()]
    menu = {}
    for i in items:
        if i[0] in menu:
            menu[i[0]].append(i[1:])
        else:
            menu[i[0]] = [i[1:]]
    # x = [(str(i) + ", " + str(i.id)).split(', ')for i in Size.objects.all()]

    category = Type.objects.all()
    #
    # context = {
    #     'items': menu.items(),
    #     'toppings': Topping.objects.all(),
    #     'user': request.user.is_authenticated,
    # }
    context = {
        'category': category
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
        'category': category
    }
        # return render(request, "pizza/index.html", context)
    return render(request, "pizza/menu.html", context)


def addFood(request):
    x = request.POST["food"]
    y = request.POST.getlist("add1")
    z = request.POST.getlist("add2")
    topping_list = request.POST.getlist("topping1")

    # topping2 = request.POST.getlist("topping2")
    # topping3 = request.POST.getlist("topping3")
    # item1 = request.POST.getlist("item1")
    # item2 = request.POST.getlist("item2")
    # item3 = request.POST.getlist("item3")
    print(z)
    print(topping_list)
    # print(topping2)
    # print(topping3)
    if y:
        price = y[0]
    else:
        price = z[0]

    if x in ['1 topping', '1 item', '2 toppings', '2 items', '3 toppings', '3 items']:
        y = x +" (" +", ".join(topping_list) +')'
        cart = Order(item=y, user=request.user, price=price)
        cart.save()
        for t in topping_list[0].split(','):
            a = Topping.objects.get(item=t)
            cart.topping.add(a)
    else:
        cart = Order(item=x, user=request.user, price=price)
        cart.save()

    return HttpResponseRedirect(reverse("index"))


def carts(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    food = [([i.item, i.price], i.id) for i in shopping]

    if request.method == "POST":
        token = request.POST.get('stripeToken', False)
        print(token)
        intent = stripe.PaymentIntent.create(
        amount=97,
        currency='usd',
        confirm=True,
        payment_method_types=["card"],
        receipt_email=request.user.email,
        metadata={'integration_check': 'accept_a_payment'},
        )

        # return HttpResponseRedirect(reverse("carts"))
    # for i in shopping:
    #     print(i.topping)

    context = {
        'food': food,
        'price': total_price
    }
    return render(request, "pizza/payment.html", context)

def payments(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})

    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)

    if request.method == "POST":
        print(request.user.email)
        # x = request.POST["token"]
        # print(x)
        token = request.POST.get('token', False)
        print(token)
        # # print(token)
        # intent = stripe.PaymentIntent.create(
        # amount=97,
        # currency='usd',
        # receipt_email=request.user.email,
        # metadata={'integration_check': 'accept_a_payment'},
        # )

        pay = stripe.Charge.create(
          amount=int(round(total_price, 2) * 100),
          currency="usd",
          source=token,
          description=request.user.email,
          receipt_email=request.user.email,
        )

        return HttpResponseRedirect(reverse("carts"))

        # stripe.PaymentIntent.confirm(
        #   "pi_1GbCB9Gj34zY5PaG5fP5LRZq",
        # )

def purchasing(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})

    shopping = Order.objects.filter(user=request.user)
    total_price = sum(float(i.price) for i in shopping)
    email_message = ''

    for i in shopping:
        Purchase(order=i.item, user=request.user, price=i.price).save()
        email_message += i.item + "  " + str(i.price) + '\n'

    email_message += 'Total price is {}'.format(str(total_price))
    # print(email_message)

    subject = "YOUR ORDER"
    from_email = settings.EMAIL_HOST_USER
    to_list = [request.user.email,]
    send_mail(subject, email_message, from_email, to_list, fail_silently=False)

    Order.objects.filter(user=request.user).delete()

    return HttpResponseRedirect(reverse("carts"))

def delete(request, item_id):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    delete_order = Order.objects.get(pk=item_id)
    delete_order.delete()

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
