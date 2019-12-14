from django.urls import path
from . import views

app_name = "feet"

urlpatterns = [
    path("measure/<int:pk>/", views.FootsizesMeasureView.as_view(), name="measure"),
]
