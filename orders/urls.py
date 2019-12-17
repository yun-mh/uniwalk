from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("check-authenticated/", views.check_authenticated, name="check-authenticated"),
    path(
        "member_or_guest/",
        views.MemberOrGuestLoginView.as_view(),
        name="member_or_guest",
    ),
    # path("checkout/", views., name="checkout"),
]
