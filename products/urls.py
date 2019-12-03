from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.ProductListView.as_view(), name="list"),
    path(
        "list/category-<int:pk>", views.ProductListView.as_view(), name="list-category"
    ),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
]
