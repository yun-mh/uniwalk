from django.urls import path
from . import views

app_name = "feet"

urlpatterns = [
    path("measure/<int:pk>/", views.footsizes_measure, name="measure"),
]
