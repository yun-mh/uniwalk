from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.ProductView.as_view(), name="list"),
    path(
        "list/category/<int:pk>",
        views.CategoryProductView.as_view(),
        name="list-category",
    ),
]
