from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signup/check/", views.SignUpCheckView.as_view(), name="signup-check"),
    path("signup/success/", views.SignupSuccessView.as_view(), name="signup-success"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "mypage/update-profile/",
        views.UpdateProfileView.as_view(),
        name="update-profile",
    ),
    path(
        "mypage/change-password/",
        views.PasswordChangeView.as_view(),
        name="change-password",
    ),
    path("mypage/orders/", views.OrdersListView.as_view(), name="orders",),
    path(
        "mypage/orders/detail/<int:order_pk>/",
        views.OrdersDetailView.as_view(),
        name="orders-detail",
    ),
    path("mypage/cards/", views.CardsListView.as_view(), name="cards",),
    path("mypage/cards/add/", views.CardsAddView.as_view(), name="add-card",),
    path("mypage/mydesigns/", views.MyDesignsListView.as_view(), name="mydesigns",),
    path("mypage/footsizes/", views.FootSizeView.as_view(), name="footsizes",),
    path("mypage/withdrawal/", views.WithdrawalView.as_view(), name="withdrawal",),
    path(
        "mypage/withdrawal/check/",
        views.WithdrawalCheckView.as_view(),
        name="withdrawal-check",
    ),
    path(
        "withdrawal/done/", views.WithdrawalDoneView.as_view(), name="withdrawal-done",
    ),
    path("switch-language/", views.switch_language, name="switch-language"),
]
