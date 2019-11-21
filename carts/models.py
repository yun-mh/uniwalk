from django.db import models
from users import models as user_models


class CartItem(models.Model):

    """ カート内のアイテムのモデルを定義する """

    # cart_id = models.ForeignKey()
    # design_id = models.ForeignKey()
    # product_id = models.ForeignKey()
    # feet_id = models.ForeignKey()
    quantity = models.IntegerField(default=1)


class Cart(models.Model):

    """ カートのモデルを定義する """

    session_key = models.CharField("カートセッションキー", max_length=32)
    created = models.DateTimeField("生成日時", auto_now_add=True)

