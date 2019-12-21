from django.db import models
from core import models as core_models
from users import models as user_models


class CartItem(models.Model):

    """ カート内のアイテムのモデルを定義する """

    cart = models.ForeignKey("Cart", related_name="cart_items", on_delete=models.CASCADE)
    # design_id = models.ForeignKey()
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    # feet_id = models.ForeignKey()
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity


class Cart(core_models.TimeStampedModel):

    """ カートのモデルを定義する """

    user = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    session_key = models.CharField("カートセッションキー", max_length=254)

