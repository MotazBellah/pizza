from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register", views.register, name='register'),
    path("signin", views.signin, name='signin'),
    path("signout", views.signout, name='signout'),
    path("carts", views.carts, name='carts'),
    path("<int:item_id>/delete", views.delete, name="delete"),
    path("addFood", views.addFood, name="addFood"),
    path("purchasing", views.purchasing, name="purchasing"),
]
