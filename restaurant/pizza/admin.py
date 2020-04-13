from django.contrib import admin
from .models import Type, Menu, Size, Topping, Order
# Register your models here.

admin.site.register(Type)
admin.site.register(Menu)
admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(Order)
