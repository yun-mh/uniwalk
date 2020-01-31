from django.urls import path
from . import views

app_name = "feet"

urlpatterns = [
    path("measure/", views.footsizes_measure, name="measure"),
    path(
        "measure/cropper/<int:pk>-left/",
        views.LeftFootsizePerspeciveCropperView.as_view(),
        name="crop-left",
    ),
    path(
        "measure/cropper/<int:pk>-right/",
        views.RightFootsizePerspeciveCropperView.as_view(),
        name="crop-right",
    ),
    path("measure/analyze/<int:pk>/", views.footsizes_analysis, name="analyze"),
]
