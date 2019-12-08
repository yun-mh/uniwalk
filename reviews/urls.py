from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("list/product-<int:pk>/", views.ReviewListView.as_view(), name="list"),
    path("product-<int:pk>/post/", views.ReviewPostView.as_view(), name="post"),
]
