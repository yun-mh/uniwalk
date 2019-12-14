from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, FormView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from django.contrib.auth import update_session_auth_hash
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
    PasswordChangeView,
)
from orders import models as order_models
from designs import models as design_models
from feet import models as feet_models
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

    def get_initial(self):
        if self.request.session.get("data"):
            return self.request.session["data"]
        else:
            return self.initial.copy()

    def form_valid(self, user):
        data = {
            "email": user.cleaned_data.get("email"),
            "password": user.cleaned_data.get("password"),
            "last_name": user.cleaned_data.get("last_name"),
            "first_name": user.cleaned_data.get("first_name"),
            "last_name_kana": user.cleaned_data.get("last_name_kana"),
            "first_name_kana": user.cleaned_data.get("first_name_kana"),
            "gender": user.cleaned_data.get("gender"),
            "member_number": user.cleaned_data.get("member_number"),
        }
        self.request.session["data"] = data
        return redirect(reverse("users:signup-check"))


class SignUpCheckView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup-check.html"

    def get(self, request):
        data = request.session.get("data")
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        data = request.session.get("data")
        user = models.User.objects.create(
            email=data["email"],
            last_name=data["last_name"],
            first_name=data["first_name"],
            last_name_kana=data["last_name_kana"],
            first_name_kana=data["first_name_kana"],
            gender=data["gender"],
            member_number=data["member_number"],
        )
        user.set_password(data["password"])
        user.member_code = "C" + data["gender"] + data["member_number"]
        user.save() 
        email = data["email"]
        html_message = render_to_string("emails/registration-done.html")
        send_mail(
            _("UniWalk　会員登録ありがとうございます。"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        del request.session["data"]
        return redirect(reverse("users:signup-success"))


class SignupSuccessView(mixins.LoggedOutOnlyView, View):
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

    def form_valid(self, form):
        email = self.user.email
        html_message = render_to_string("emails/password-reset-done.html")
        send_mail(
            _("パスワード再設定完了のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password-reset-complete.html"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    form_class = forms.UpdateProfileForm
    template_name = "users/update-profile.html"
    success_message = _("会員情報を変更しました。")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return reverse("users:update-profile", kwargs={"pk": pk})

    def form_valid(self, form):
        user = form.save()
        user.save()
        email = form.cleaned_data.get("email")
        html_message = render_to_string("emails/profile-change-done.html")
        send_mail(
            _("UniWalk会員情報変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        return super().form_valid(form)


class PasswordChangeView(mixins.LoggedInOnlyView, PasswordChangeView):
    form_class = forms.PasswordChangeForm
    template_name = 'users/password-change.html'

    def form_valid(self, form):
        form.save()
        email = self.request.user.email
        html_message = render_to_string("emails/password-change-done.html")
        send_mail(
            _("UniWalkパスワード変更のお知らせ"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, _(f"パスワードを変更しました。"))
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return reverse("users:update-profile", kwargs={"pk": pk})


class OrdersListView(mixins.LoggedInOnlyView, ListView):
    model = order_models.Order
    template_name = "orders/order-list.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        try:
            return order_models.Order.objects.filter(user_id=self.kwargs.get("pk"))
        except order_models.Order.DoesNotExist:
            return None


class OrdersDetailView(mixins.LoggedInOnlyView, DetailView):

    """ 注文詳細 """

    model = order_models.Order
    template_name = "orders/order-detail.html"
    pk_url_kwarg = "order_pk"


class MyDesignsListView(mixins.LoggedInOnlyView, ListView):
    model = design_models.Design
    template_name = "designs/design-list.html"
    context_object_name = "designs"
    paginate_by = 5

    def get_queryset(self):
        try:
            return design_models.Design.objects.filter(user_id=self.kwargs.get("pk"))
        except design_models.Design.DoesNotExist:
            return None


class FootSizeView(mixins.LoggedInOnlyView, ListView):
    model = feet_models.Footsize
    template_name = "feet/feet-list.html"
    context_object_name = "feet"

    def get_queryset(self):
        try:
            return feet_models.Footsize.objects.get(user_id=self.kwargs.get("pk"))
        except feet_models.Footsize.DoesNotExist:
            return None

class WithdrawalView(mixins.LoggedInOnlyView, FormView):
    template_name = "users/withdrawal.html"
    form_class = forms.WithdrawalForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        email = form.cleaned_data.get("email")
        if self.request.user.email != email:
            messages.error(self.request, _("会員様のメールアドレスと入力したメールアドレスが違います。"))
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
