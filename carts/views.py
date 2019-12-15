from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from products import models as product_models
from .models import Cart, CartItem


def _session_key(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, pk):
    product = product_models.Product.objects.get(pk=pk)
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=_session_key(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect("carts:cart")


def cart_display(request, amount=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            amount += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(
        request,
        "carts/cart.html",
        {"cart_items": cart_items, "amount": amount, "counter": counter},
    )
