from django.http import HttpResponse
from django.shortcuts import render
from .models import Size

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

    # print(menu['Regular Pizza'])
    # print(menu['Sicilian Pizza'])
    for i in menu.items():
        print(i)
    context = {
        'items': menu.items()
    }

    return render(request, "pizza/index.html", context)
