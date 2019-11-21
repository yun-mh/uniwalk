from django.db import models
from core import models as core_models


class Image(core_models.TimeStampedModel):

    """ 商品のイメージを管理するモデルを定義する """

    product_id = models.ForeignKey(
        "Product", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="product_images")


class Category(core_models.TimeStampedModel):

    """ 商品カテゴリーのためのモデル """

    product_type = models.CharField("商品タイプ名", max_length=20)
    type_code = models.CharField("タイプコード", max_length=2)

class Product(core_models.TimeStampedModel):

    """ 商品のモデルを定義する """

    TYPE_HIGH = "H"
    TYPE_MID = "M"
    TYPE_LOW = "L"

    TYPE_CHOICES = ((TYPE_HIGH, "ハイカット"), (TYPE_MID, "ミドルカット"), (TYPE_LOW, "ローカット"))

    name = models.CharField("商品名", max_length=50)
    type = models.CharField("商品種別", choices=TYPE_CHOICES, max_length=1)
    # category_id = models.CharField("商品カテゴリー", max_length=10)
    price = models.IntegerField("価格", default=0)
    description = models.TextField("詳細説明")
    is_active = models.BooleanField("販売中", null=False, default=True)
    product_code = models.CharField("商品番号", max_length=5)
