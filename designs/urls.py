from django.urls import path
from . import views

app_name = "designs"

urlpatterns = [
    path("customize/<int:pk>/", views.CustomizeView.as_view(), name="customize"),
    path("apply/", views.get_palette, name="apply"),
]
