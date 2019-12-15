from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("add/<int:pk>/", views.add_cart, name="add_cart"),
    path("", views.cart_display, name="cart"),
]
