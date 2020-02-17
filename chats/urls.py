from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("guest/", views.guestUser, name="guest"),
    path("pusher/auth/", views.pusher_authentication, name="auth"),
]
