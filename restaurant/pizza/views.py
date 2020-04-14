from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Size, Topping, Order, Menu
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
        topping1 = request.POST.getlist("topping1")
        topping2 = request.POST.getlist("topping2")
        topping3 = request.POST.getlist("topping3")
        item1 = request.POST.getlist("item11")
        item2 = request.POST.getlist("item2")
        item3 = request.POST.getlist("item3")

        if topping1:
            adding_one_topping = Menu.objects.get(item='1 topping')
            # print(food_menu)
            one_topping = Topping.objects.get(item=topping1[-1])
            one_topping.menu.add(adding_one_topping)
            # print(adds.menu.all())
            print('ONE')
            print(adding_one_topping.menu.all())

        if topping2:
            adding_two_topping = Menu.objects.get(item='2 toppings')
            # print(food_menu)
            for i in topping2:
                adds = Topping.objects.get(item=i)
                adds.menu.add(adding_two_topping)
            # print(adds.menu.all())
            print('TWO')
            print(adding_two_topping.menu.all())

        if topping3:
            adding_three_topping = Menu.objects.get(item='3 toppings')
            # print(food_menu)
            for i in topping3:
                adds = Topping.objects.get(item=i)
                adds.menu.add(adding_three_topping)
            # print(adds.menu.all())
            print('THREE')
            print(adding_three_topping.menu.all())

        if item1:
            adding_one_item = Menu.objects.get(item='1 item')
            # print(food_menu)
            adds = Topping.objects.get(item=item1[-1])
            adds.menu.add(adding_one_item)
            # print(adds.menu.all())
            print(adding_one_item.menu.all())

        if item2:
            adding_two_item = Menu.objects.get(item='2 items')
            # print(food_menu)
            for i in item2:
                adds = Topping.objects.get(item=i)
                adds.menu.add(adding_two_item)
            # print(adds.menu.all())
            print(adding_two_item.menu.all())

        if item3:
            adding_three_item = Menu.objects.get(item='3 items')
            # print(food_menu)
            for i in item3:
                adds = Topping.objects.get(item=i)
                adds.menu.add(adding_three_item)
            # print(adds.menu.all())
            print(adding_three_item.menu.all())

        if prices:
            total = sum(float(i) for i in prices)
            food_price = list(zip(items, prices))
            for i in food_price:

                # print(a.menu.all())
                if i[0] in ['1 topping', "1 item", '2 toppings', '2 items', '3 toppings', '3 items']:
                    a = Menu.objects.get(item=i[0])
                    all = a.menu.all()
                    s, e = 0, 0
                    while e < len(all):
                        if i[0] in ['1 topping', "1 item"]:
                            s, e = e, e+1
                        if i[0] in ['2 toppings', '2 items']:
                            s, e = e, e+2
                        if i[0] in ['3 toppings', '3 items']:
                            s, e = e, e+3
                        z = ", ".join([i.item for i in all[s:e]])
                        print(z)
                    y = i[0] + ' ('+ z +')'
                    cart = Order(item=y, user=current_user, price=i[1])
                    cart.save()
                else:
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
