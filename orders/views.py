from django.shortcuts import render, redirect, reverse
from django.views.generic import View, FormView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
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

        recipient_info = user_models.User.objects.filter(email=self.request.user)
        if recipient_info.exists:
            context.update({"recipient_info": recipient_info})

        return render(self.request, "orders/checkout.html", context)

    def post(self, *args, **kwargs):
        recipient_form = forms.CheckoutForm(self.request.POST)
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
        if orderer_form.is_valid():
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
        models.Order.objects.create(
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
        cart_items.update(active=False)
        print(self.request.session.session_key)
        self.request.session.cycle_key_after_purchase()
        print(self.request.session.session_key)
        return redirect("orders:checkout-done")


class CheckoutDoneView(View):
    def get(self, request):
        return render(request, "orders/checkout-done.html")
