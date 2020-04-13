from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from .models import Size, Topping

# Create your views here.
def index(request):
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
        'toppings': Topping.objects.all()
    }
    return render(request, "pizza/index.html", context)


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
    logout(request)
    return render(request, "pizza/login.html", {"message": "Logged out."})
