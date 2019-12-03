from django.db import models
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):

    """ レビューのモデルを定義する """

    product = models.ForeignKey(
        "products.Product",
        verbose_name="商品",
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "users.User", verbose_name="ユーザー", on_delete=models.CASCADE
    )
    title = models.CharField("タイトル", max_length=50)
    text = models.TextField("本文")
    rate = models.IntegerField("評点", default=0)
    review_code = models.CharField("レビュー番号", max_length=11, default="test")

    class Meta:
        verbose_name = "レビュー"
        verbose_name_plural = "レビュー"

    def __str__(self):
        return self.title
