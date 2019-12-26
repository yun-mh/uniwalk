from django.shortcuts import render, redirect, reverse, render_to_response
from django.views.generic import View, FormView, DetailView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from users import mixins
from users import forms as user_forms
from users import models as user_models
from carts import models as cart_models
from . import forms, models


def member_or_guest_login(request):
    if request.user.is_authenticated:
        return redirect("orders:checkout")
    if request.method == "POST":
        if "member_login" in request.POST:
            member_form = user_forms.LoginForm(request.POST, prefix="member")
            if member_form.is_valid():
                member_email = member_form.cleaned_data.get("email")
                member_password = member_form.cleaned_data.get("password")
                user = authenticate(
                    request, email=member_email, password=member_password
                )
                if user is not None:
                    login(request, user)
                    return redirect(reverse("orders:checkout"))
            guest_form = forms.GuestForm(prefix="guest")
        elif "guest_login" in request.POST:
            guest_form = forms.GuestForm(request.POST, prefix="guest")
            if guest_form.is_valid():
                guest_email = guest_form.cleaned_data.get("email")
                try:
                    user_models.Guest.objects.get(email=guest_email)
                except user_models.Guest.DoesNotExist:
                    user_models.Guest.objects.create(email=guest_email)
                request.session["guest_email"] = guest_email
                return redirect(reverse("orders:checkout"))
            member_form = user_forms.LoginForm(prefix="member")
    else:
        guest_form = forms.GuestForm(prefix="guest")
        member_form = user_forms.LoginForm(prefix="member")
    context = {"member_form": member_form, "guest_form": guest_form}
    return render(request, "orders/member-or-guest.html", context)


class CheckoutView(FormView):
    def get(self, *args, **kwargs):
        recipient_form = forms.CheckoutForm()
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_form": recipient_form,
            "cart": cart,
            "total": total,
        }
        if self.request.user.is_authenticated:
            recipient = user_models.User.objects.get(email=self.request.user).as_dict()
            print(recipient)
            context["recipient_info"] = recipient

        return render(self.request, "orders/checkout.html", context)

    def post(self, *args, **kwargs):
        recipient_form = forms.CheckoutForm(self.request.POST)
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_form": recipient_form,
            "cart": cart,
            "total": total,
        }
        if recipient_form.is_valid():
            recipient_data = {
                "last_name_recipient": recipient_form.cleaned_data.get(
                    "last_name_recipient"
                ),
                "first_name_recipient": recipient_form.cleaned_data.get(
                    "first_name_recipient"
                ),
                "last_name_recipient_kana": recipient_form.cleaned_data.get(
                    "last_name_recipient_kana"
                ),
                "first_name_recipient_kana": recipient_form.cleaned_data.get(
                    "first_name_recipient_kana"
                ),
                "phone_number_recipient": recipient_form.cleaned_data.get(
                    "phone_number_recipient"
                ),
                "postal_code_recipient": recipient_form.cleaned_data.get(
                    "postal_code_recipient"
                ),
                "prefecture_recipient": recipient_form.cleaned_data.get(
                    "prefecture_recipient"
                ),
                "address_city_recipient": recipient_form.cleaned_data.get(
                    "address_city_recipient"
                ),
                "address_detail_recipient": recipient_form.cleaned_data.get(
                    "address_detail_recipient"
                ),
            }
            self.request.session["recipient_data"] = recipient_data
            return redirect(reverse("orders:select-payment"))
        return render(self.request, "orders/checkout.html", context)

class SelectPaymentView(FormView):
    def get(self, *args, **kwargs):
        orderer_form = forms.SelectPaymentForm()
        recipient_data = self.request.session["recipient_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_data": recipient_data,
            "orderer_form": orderer_form,
            "cart": cart,
            "total": total,
        }

        # card?

        return render(self.request, "orders/select-payment.html", context)

    def post(self, *args, **kwargs):
        orderer_form = forms.SelectPaymentForm(self.request.POST)
        recipient_data = self.request.session["recipient_data"]
        if orderer_form.is_valid():
            if orderer_form.cleaned_data.get("is_same_with_recipient") == True:
                orderer_data = {
                    "is_same_with_recipient": orderer_form.cleaned_data.get(
                        "is_same_with_recipient"
                    ),
                    "payment": orderer_form.cleaned_data.get("payment"),
                    "last_name_orderer": recipient_data["last_name_recipient"],
                    "first_name_orderer": recipient_data["first_name_recipient"],
                    "last_name_orderer_kana": recipient_data["last_name_recipient_kana"],
                    "first_name_orderer_kana": recipient_data["first_name_recipient_kana"],
                    "phone_number_orderer": recipient_data["phone_number_recipient"],
                    "postal_code_orderer": recipient_data["postal_code_recipient"],
                    "prefecture_orderer": recipient_data["prefecture_recipient"],
                    "address_city_orderer": recipient_data["address_city_recipient"],
                    "address_detail_orderer": recipient_data["address_detail_recipient"],
                }
            else:
                orderer_data = {
                    "is_same_with_recipient": orderer_form.cleaned_data.get(
                        "is_same_with_recipient"
                    ),
                    "payment": orderer_form.cleaned_data.get("payment"),
                    "last_name_orderer": orderer_form.cleaned_data.get("last_name_orderer"),
                    "first_name_orderer": orderer_form.cleaned_data.get(
                        "first_name_orderer"
                    ),
                    "last_name_orderer_kana": orderer_form.cleaned_data.get(
                        "last_name_orderer_kana"
                    ),
                    "first_name_orderer_kana": orderer_form.cleaned_data.get(
                        "first_name_orderer_kana"
                    ),
                    "phone_number_orderer": orderer_form.cleaned_data.get(
                        "phone_number_orderer"
                    ),
                    "postal_code_orderer": orderer_form.cleaned_data.get(
                        "postal_code_orderer"
                    ),
                    "prefecture_orderer": orderer_form.cleaned_data.get(
                        "prefecture_orderer"
                    ),
                    "address_city_orderer": orderer_form.cleaned_data.get(
                        "address_city_orderer"
                    ),
                    "address_detail_orderer": orderer_form.cleaned_data.get(
                        "address_detail_orderer"
                    ),
                }
            self.request.session["orderer_data"] = orderer_data
            return redirect(reverse("orders:order-check"))


class OrderCheckView(FormView):
    def get(self, *args, **kwargs):
        recipient_data = self.request.session["recipient_data"]
        orderer_data = self.request.session["orderer_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "recipient_data": recipient_data,
            "orderer_data": orderer_data,
            "cart": cart,
            "total": total,
        }
        return render(self.request, "orders/order-check.html", context)

    def post(self, *args, **kwargs):
        recipient_data = self.request.session["recipient_data"]
        orderer_data = self.request.session["orderer_data"]
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        if self.request.user.is_authenticated:
            user = self.request.user
            guest = None
        else:
            user = None
            guest = user_models.Guest.objects.filter(
                email=self.request.session["guest_email"]
            ).first()
        new_order = models.Order.objects.create(
            user=user,
            guest=guest,
            last_name_recipient=recipient_data["last_name_recipient"],
            first_name_recipient=recipient_data["first_name_recipient"],
            last_name_recipient_kana=recipient_data["last_name_recipient_kana"],
            first_name_recipient_kana=recipient_data["first_name_recipient_kana"],
            phone_number_recipient=recipient_data["phone_number_recipient"],
            postal_code_recipient=recipient_data["postal_code_recipient"],
            prefecture_recipient=recipient_data["prefecture_recipient"],
            address_city_recipient=recipient_data["address_city_recipient"],
            address_detail_recipient=recipient_data["address_detail_recipient"],
            last_name_orderer=orderer_data["last_name_orderer"],
            first_name_orderer=orderer_data["first_name_orderer"],
            last_name_orderer_kana=orderer_data["last_name_orderer_kana"],
            first_name_orderer_kana=orderer_data["first_name_orderer_kana"],
            phone_number_orderer=orderer_data["phone_number_orderer"],
            postal_code_orderer=orderer_data["postal_code_orderer"],
            prefecture_orderer=orderer_data["prefecture_orderer"],
            address_city_orderer=orderer_data["address_city_orderer"],
            address_detail_orderer=orderer_data["address_detail_orderer"],
            payment=orderer_data["payment"],
            amount=total,
        )
        try:
            email = self.request.user.email
        except:
            email = self.request.session["guest_email"]
        order_code = new_order.order_code
        cart_items.update(active=False)
        self.request.session.cycle_key_after_purchase()
        html_message = render_to_string("emails/purchase-done.html", {"order_code": order_code})
        send_mail(
            _("UniWalk　ご注文ありがとうございます。"),
            strip_tags(html_message),
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        try:
            del self.request.session["guest_email"]
            del self.request.session["recipient_data"]
            del self.request.session["orderer_data"]
        except:
            pass
        return redirect("orders:checkout-done", order_code)


class CheckoutDoneView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "order_code": kwargs.get("order_code")
        }
        return render(request, "orders/checkout-done.html", context)


class OrderSearchView(FormView):
    model = models.Order
    form_class = forms.OrderSearchForm
    template_name = "orders/order-search.html"
    success_url = reverse_lazy("orders:detail")

    def form_valid(self, form):
        order_code = form.cleaned_data.get("order_code")
        email = form.cleaned_data.get("email")
        try:
            order = models.Order.objects.get(order_code=order_code)
        except models.Order.DoesNotExist:
            messages.error(self.request, _("入力した情報をもう一度確認してください。"))
            return redirect("orders:search")
        if str(order.user) != email and str(order.guest.email) != email:
            messages.error(self.request, _("入力した情報をもう一度確認してください。"))
            return redirect("orders:search")
        else:
            return redirect("orders:detail", order_code)


class OrderDetailView(DetailView):
    template_name = "orders/search-order-detail.html"
    context_object_name = "order"
    slug_field = 'order_code'
    slug_url_kwarg = 'order_code'

    def get_queryset(self):
        order_code = self.kwargs.get("order_code")
        try:
            return models.Order.objects.filter(order_code=order_code)
        except models.Order.DoesNotExist:
            return None

