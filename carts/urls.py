from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart_display, name="cart"),
    path(
        "add/<int:pk>/<int:design_pk>/<int:foot_pk>/", views.add_cart, name="add_cart"
    ),
    path(
        "remove/<int:pk>/<int:design_pk>/<int:foot_pk>/",
        views.remove_item,
        name="remove",
    ),
    path(
        "delete-item/<int:pk>/<int:design_pk>/<int:foot_pk>/",
        views.delete_cartitem,
        name="delete",
    ),
]
