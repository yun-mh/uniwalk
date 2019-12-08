from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
    )
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user


class WithdrawalView(mixins.LoggedInOnlyView, FormView):
    template_name = "users/withdrawal.html"
    form_class = forms.WithdrawalForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        email = form.cleaned_data.get("email")
        if self.request.user.email != email:
            messages.error(self.request, "会員様のメールアドレスと入力したメールアドレスが違います。")
            return redirect(reverse("users:withdrawal", kwargs={"pk": pk}))
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return reverse("users:withdrawal-check", kwargs={"pk": pk})


class WithdrawalCheckView(mixins.LoggedInOnlyView, DeleteView):
    model = models.User
    template_name = "users/withdrawal-check.html"

    def get(self, request, pk):
        return render(request, self.template_name, {"pk": pk})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    # def delete(self, form):
    #     pk = self.kwargs.get("pk")
    #     print(pk)
    #     try:
    #         user = models.User.objects.get(pk=pk)
    #         print(user)
    #         user.delete()
    #     except models.User.DoesNotExist:
    #         messages.error(self.request, "会員脱退を失敗しました。")
    #         return redirect(reverse("users:withdrawal", kwargs={"pk": pk}))
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:withdrawal-done")


class WithdrawalDoneView(View):
    template_name = "users/withdrawal-done.html"

    def get(self, request):
        return render(request, template_name=self.template_name)



def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
