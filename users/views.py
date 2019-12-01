from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import forms, models, mixins

# Create your views here.
class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, _(f"ログインしました。"))
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, _("ログアウトしました。"))
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("users:signup-success")

    def form_valid(self, form):
        form.save()
        # email = form.cleaned_data.get("email")
        # password = form.cleaned_data.get("password")
        # user = authenticate(self.request, email=email, password=password)
        # if user is not None:
        # login(self.request, user)
        # user.verify_email()
        return super().form_valid(form)


class SignupSuccessView(View):
    def get(self, request):
        return render(request, "users/signup-success.html")

