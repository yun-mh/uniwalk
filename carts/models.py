from django.db import models
from django.utils.translation import ugettext_lazy as _
from core import models as core_models
from users import models as user_models


class CartItem(models.Model):

    """ カート内のアイテムのモデルを定義する """

    cart = models.ForeignKey(
        "Cart",
        related_name="cart_items",
        verbose_name=_("カート"),
        on_delete=models.CASCADE,
    )
    design = models.ForeignKey(
        "designs.Design",
        verbose_name=_("デザイン"),
        related_name="cart_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        "products.Product", verbose_name=_("商品"), on_delete=models.CASCADE
    )
    length_left = models.DecimalField(_("足長(左)"), max_digits=4, decimal_places=1)
    length_right = models.DecimalField(_("足長(右)"), max_digits=4, decimal_places=1)
    width_left = models.DecimalField(_("足幅(左)"), max_digits=4, decimal_places=1)
    width_right = models.DecimalField(_("足幅(右)"), max_digits=4, decimal_places=1)
    quantity = models.IntegerField(_("数量"), default=1)
    active = models.BooleanField(_("活性化"), default=True)

    def sub_total(self):
        return self.product.price * self.quantity


class Cart(core_models.TimeStampedModel):

    """ カートのモデルを定義する """

    user = models.ForeignKey(
        "users.User", null=True, verbose_name=_("会員"), on_delete=models.CASCADE
    )
    session_key = models.CharField(_("カートセッションキー"), max_length=254)

