from django.urls import path
from . import views

app_name = "designs"

urlpatterns = [
    path("customize/<int:pk>/", views.CustomizeView.as_view(), name="customize"),
    path("apply/", views.get_palette, name="apply"),
    path("gallery/", views.GalleriesListView.as_view(), name="galleries"),
    path(
        "gallery/category-<int:pk>/",
        views.GalleriesListByCategoryView.as_view(),
        name="galleries-category",
    ),
    path(
        "gallery/product-<int:pk>/",
        views.GalleriesListByProductView.as_view(),
        name="galleries-product",
    ),
    path("gallery/like/", views.design_like, name="like"),
]
