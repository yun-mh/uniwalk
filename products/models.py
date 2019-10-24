from django.db import models
from core import models as core_models


class Image(core_models.TimeStampedModel):

    """ 商品のイメージを管理するモデルを定義する """

    file = models.ImageField(upload_to="product_images")
    product = models.ForeignKey(
        "Product", related_name="images", on_delete=models.CASCADE
    )


class Product(core_models.TimeStampedModel):

    """ 商品のモデルを定義する """

    TYPE_HIGH = "H"
    TYPE_MID = "M"
    TYPE_LOW = "L"

    TYPE_CHOICES = ((TYPE_HIGH, "ハイカット"), (TYPE_MID, "ミドルカット"), (TYPE_LOW, "ローカット"))

    code = models.CharField("商品番号", max_length=5)
    name = models.CharField("商品名", max_length=50)
    type = models.CharField("商品種別", choices=TYPE_CHOICES, max_length=1)
    price = models.IntegerField("価格", default=0)
    description = models.TextField("説明")
