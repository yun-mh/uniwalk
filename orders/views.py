from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from users import mixins
from users import forms as user_forms


def check_authenticated(request):
    if not request.user.is_authenticated:
        return redirect("orders:member_or_guest")
    return redirect("core:home")  # すぐ注文情報入力へ


class MemberOrGuestLoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "orders/member_or_guest.html"
    form_class = user_forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")
