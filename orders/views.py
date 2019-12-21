from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from users import mixins
from users import forms as user_forms
from users import models as user_models
from carts import models as cart_models
from . import forms


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
                return redirect(reverse("orders:checkout"))
            member_form = user_forms.LoginForm(prefix="member")
    else:
        guest_form = forms.GuestForm(prefix="guest")
        member_form = user_forms.LoginForm(prefix="member")
    context = {"member_form": member_form, "guest_form": guest_form}
    return render(request, "orders/member_or_guest.html", context)


class CheckoutView(FormView):
    def get(self, *args, **kwargs):
        form = forms.CheckoutForm()
        cart = cart_models.Cart.objects.get(
            session_key=self.request.session.session_key
        )
        cart_items = cart_models.CartItem.objects.filter(cart=cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
        context = {
            "form": form,
            "cart": cart,
            "total": total,
        }
        return render(self.request, "orders/checkout.html", context)

    def post(self, *args, **kwargs):
        form = forms.CheckoutForm(self.request.POST)
        if form.is_valid():
            print("gooood")
            return redirect("orders:checkout")

