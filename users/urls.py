from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
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
        "mypage/<int:pk>/update-profile",
        views.UpdateProfileView.as_view(),
        name="update-profile",
    ),
    # path(
    #     "mypage/<int:pk>/profile/update/",
    #     views.UpdateProfileView.as_view(),
    #     name="update-profile",
    # ),
    # path("mypage/<int:pk>/orders/", views.OrdersListView.as_view(), name="orders",),
    # path(
    #     "mypage/<int:user_pk>/orders/detail/<int:order_pk>",
    #     views.OrdersDetailView.as_view(),
    #     name="orders-detail",
    # ),
    # path("mypage/<int:pk>/cards/", views.CardsListView.as_view(), name="cards",),
    # path(
    #     "mypage/<int:pk>/mydesigns/",
    #     views.MyDesignsListView.as_view(),
    #     name="mydesigns",
    # ),
    # path("mypage/<int:pk>/footsizes/", views.FootSizeView.as_view(), name="footsizes",),
    path(
        "mypage/<int:pk>/withdrawal/",
        views.WithdrawalView.as_view(),
        name="withdrawal",
    ),
    path(
        "mypage/<int:pk>/withdrawal/check/",
        views.WithdrawalCheckView.as_view(),
        name="withdrawal-check",
    ),
    path("switch-language/", views.switch_language, name="switch-language"),
]
