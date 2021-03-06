from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("member_or_guest/", views.member_or_guest_login, name="member_or_guest"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/payment/", views.SelectPaymentView.as_view(), name="select-payment"),
    path("checkout/check/", views.OrderCheckView.as_view(), name="order-check"),
    path(
        "checkout/done/<str:order_code>",
        views.CheckoutDoneView.as_view(),
        name="checkout-done",
    ),
    path("search/", views.OrderSearchView.as_view(), name="search"),
    path("detail/<str:order_code>/", views.OrderDetailView.as_view(), name="detail"),
    path("receipt/<str:order_code>/", views.ReceiptView.as_view(), name="receipt"),
    path("bill/<str:order_code>/", views.BillView.as_view(), name="bill"),
]
