from .models import Cart, CartItem
from .views import _session_key


def counter(request):
    item_count = 0
    if "admin" in request.META["PATH_INFO"]:
        return {}
    else:
        try:
            cart = Cart.objects.get(session_key=_session_key(request))
            cart_items = CartItem.objects.all().filter(cart=cart, active=True)
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)

