from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Size, Topping, Order
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    # context = {
    #     'items': [str(i).split(', ') for i in Size.objects.all()]
    # }
    items = [str(i).split(', ') for i in Size.objects.all()]
    menu = {}
    for i in items:
        if i[0] in menu:
            menu[i[0]].append(i[1:])
        else:
            menu[i[0]] = [i[1:]]

    context = {
        'items': menu.items(),
        'toppings': Topping.objects.all(),
        'user': request.user.is_authenticated
    }
    return render(request, "pizza/index.html", context)


def foodOrder(request):
    if request.method == "POST":
        prices = request.POST.getlist("checkbox")
        items = request.POST.getlist("food")
        current_user = request.user
        topping = request.POST.getlist("topping")
        print(topping)
        # print(request.POST["items"])
        # items = request.args.get('items')
        # print(prices)
        print(items)
        if prices:
            total = sum(float(i) for i in prices)
            food_price = list(zip(items, prices))
            for i in food_price:
                j = i[0] + ',' + i[1]
                cart = Order(item=i[0], user=current_user, price=i[1])
                cart.save()
        return HttpResponseRedirect(reverse("index"))


def carts(request):
    if not request.user.is_authenticated:
        return render(request, "pizza/login.html", {"message":None})
    shopping = Order.objects.all()
    total_price = sum(float(i.price) for i in shopping)
    food = [([i.item, i.price], i.id) for i in shopping]
    context = {
        'food': food,
        'price': total_price
    }
    return render(request, "pizza/cart.html", context)

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
