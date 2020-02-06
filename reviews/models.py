from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):

    """ レビューのモデルを定義する """

    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("商品"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User", verbose_name=_("ユーザー"), on_delete=models.CASCADE
    )
    title = models.CharField(_("タイトル"), max_length=50)
    text = models.TextField(_("本文"))
    rate = models.PositiveIntegerField(
        _("評点"), default=0, validators=[MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = _("レビュー")
        verbose_name_plural = _("レビュー")

    def __str__(self):
        return self.title
