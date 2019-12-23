from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # path("check-authenticated/", views.check_authenticated, name="check-authenticated"),
    path("member_or_guest/", views.member_or_guest_login, name="member_or_guest"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/payment/", views.SelectPaymentView.as_view(), name="select-payment"),
    path("checkout/check/", views.OrderCheckView.as_view(), name="order-check"),
    path("checkout/done/", views.CheckoutDoneView.as_view(), name="checkout-done"),
]
