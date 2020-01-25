from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from designs import models as design_models
from feet import models as foot_models
from products import models as product_models
from .models import Cart, CartItem


# 現在のセッション宛にカートを生成するための関数
def _session_key(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, pk, design_pk, foot_pk):

    """ カートに商品を追加するビュー """

    product = product_models.Product.objects.get(pk=pk)
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
    except Cart.DoesNotExist:
        if request.user.is_authenticated:
            cart = Cart.objects.create(
                session_key=_session_key(request), user_id=request.user.pk
            )
            cart.save()
        else:
            cart = Cart.objects.create(session_key=_session_key(request))
            cart.save()
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, design=design_pk, feet=foot_pk
        )
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            design=design_models.Design.objects.get(pk=design_pk),
            feet=foot_models.Footsize.objects.get(pk=foot_pk),
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect("carts:cart")


def cart_display(request, amount=0, counter=0, cart_items=None):
    
    """ カートの内容を表示するためのビュー """
    
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart)
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


def remove_item(request, pk, design_pk, foot_pk):

    """ カートに入れた商品の個数を減少させるためのビュー """

    cart = Cart.objects.get(session_key=_session_key(request))
    product = get_object_or_404(product_models.Product, pk=pk)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, design=design_pk, feet=foot_pk
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("carts:cart")


def delete_cartitem(request, pk, design_pk, foot_pk):

    """ 商品項目をカートから削除するためのビュー """

    cart = Cart.objects.get(session_key=_session_key(request))
    product = get_object_or_404(product_models.Product, pk=pk)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, design=design_pk, feet=foot_pk
    )
    cart_item.delete()
    return redirect("carts:cart")
