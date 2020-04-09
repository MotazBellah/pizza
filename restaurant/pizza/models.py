from django.db import models

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Menu(models.Model):
    item = models.CharField(max_length=64)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.item} ({self.type})"


class Size(models.Model):
    small = models.FloatField(default=0.0)
    large = models.FloatField(default=0.0)
    menu = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.small} {self.large}"


class Topping(models.Model):
    item = models.FloatField(default=0.0)
    menu = models.ManyToManyField(Menu, blank=True, related_name='passengers')

    def __str__(self):
        return f"{self.item}"
