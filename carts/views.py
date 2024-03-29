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


def add_cart(request, pk, design_pk):

    """ カートに商品を追加するビュー """

    product = product_models.Product.objects.get(pk=pk)
    # カートを持っているかチェック
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
    # 持っていない場合、カートを生成する
    except Cart.DoesNotExist:
        if request.user.is_authenticated:
            cart = Cart.objects.create(
                session_key=_session_key(request), user_id=request.user.pk
            )
            cart.save()
        else:
            cart = Cart.objects.create(session_key=_session_key(request))
            cart.save()
    # カート内に同じ商品かつ同じデザインのアイテムがあるかチェック
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, design=design_pk)
        # 取得したアイテムのサイズとセッションのサイズ値が違う場合、ブラウザの前ボタンでサイズを修正したことのため、サイズのみをアップデートする
        if (
            cart_item.length_left != request.session["length_left"]
            or cart_item.length_right != request.session["length_right"]
            or cart_item.width_left != request.session["width_left"]
            or cart_item.width_right != request.session["width_right"]
        ):
            cart_item.length_left = request.session["length_left"]
            cart_item.length_right = request.session["length_right"]
            cart_item.width_left = request.session["width_left"]
            cart_item.width_right = request.session["width_right"]
        # サイズも同じな場合は全く同じ商品の追加になるため、数量を増やす
        else:
            cart_item.quantity += 1
        cart_item.save()
    # ない場合、新しくカートアイテムを生成する
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            design=design_models.Design.objects.get(pk=design_pk),
            length_left=request.session["length_left"],
            length_right=request.session["length_right"],
            width_left=request.session["width_left"],
            width_right=request.session["width_right"],
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect("carts:cart")


def cart_display(request, amount=0, counter=0, cart_items=None):

    """ カートの内容を表示するためのビュー """

    # セッションキーに対しカートが既に存在する場合
    try:
        cart = Cart.objects.get(session_key=_session_key(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            amount += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    # カートが存在しない場合
    except ObjectDoesNotExist:
        pass
    return render(
        request,
        "carts/cart.html",
        {"cart_items": cart_items, "amount": amount, "counter": counter},
    )


def remove_item(request, pk, design_pk):

    """ カートに入れた商品の個数を減少させるためのビュー """

    # データベースから関連項目を取得する
    cart = Cart.objects.get(session_key=_session_key(request))
    product = get_object_or_404(product_models.Product, pk=pk)
    cart_item = CartItem.objects.get(product=product, cart=cart, design=design_pk)
    # 削除しようとするカートアイテムの数が1より多い場合
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    # 削除しようとするカートアイテムの数が1以下の場合
    else:
        cart_item.delete()
    return redirect("carts:cart")


def delete_cartitem(request, pk, design_pk):

    """ 商品項目をカートから削除するためのビュー """

    # データベースから関連項目を取得し、対象カートアイテムを削除する
    cart = Cart.objects.get(session_key=_session_key(request))
    product = get_object_or_404(product_models.Product, pk=pk)
    cart_item = CartItem.objects.get(product=product, cart=cart, design=design_pk)
    cart_item.delete()
    return redirect("carts:cart")
