from django.db import models
from users import models as user_models


class CartItem(models.Model):

    """ カート内のアイテムのモデルを定義する """

    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    # design_id = models.ForeignKey()
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    # feet_id = models.ForeignKey()
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity


class Cart(models.Model):

    """ カートのモデルを定義する """

    session_key = models.CharField("カートセッションキー", max_length=254)
    created = models.DateTimeField("生成日時", auto_now_add=True)

