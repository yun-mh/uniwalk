from django.urls import path
from . import views

app_name = "feet"

urlpatterns = [
    path("measure/", views.footsizes_measure, name="measure"),
]
