from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Menu(models.Model):
    item = models.CharField(max_length=64)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type}, {self.item}"


class Size(models.Model):
    small = models.FloatField(default=0.0)
    large = models.FloatField(default=0.0)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu}, {self.small}, {self.large}"


class Topping(models.Model):
    item = models.CharField(max_length=64)
    menu = models.ManyToManyField(Menu, blank=True, related_name='menu')

    def __str__(self):
        return f"{self.item}, {self.menu}"


class Order(models.Model):
    item = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user}, {self.item}, {self.price}"
