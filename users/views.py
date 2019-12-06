from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
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
        email = form.cleaned_data.get("email")
        html_message = render_to_string("emails/registration-done.html")
        send_mail(
            _("UniWalk　会員登録ありがとうございます。"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class SignupSuccessView(View):
    def get(self, request):
        return render(request, "users/signup-success.html")


class PasswordResetView(PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = "users/password-reset.html"
    subject_template_name = "emails/password-reset-subject.txt"
    email_template_name = "emails/password-reset-email.html"
    success_url = reverse_lazy("users:password-reset-done")


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    template_name = "users/password-reset-confirm.html"
    success_url = reverse_lazy("users:password-reset-complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password-reset-complete.html"


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
