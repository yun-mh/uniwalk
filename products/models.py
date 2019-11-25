from django.db import models
from core import models as core_models


class Image(core_models.TimeStampedModel):

    """ 商品のイメージを管理するモデルを定義する """

    product = models.ForeignKey(
        "Product", verbose_name="商品", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField("イメージ", upload_to="product_images")


class Category(core_models.TimeStampedModel):

    """ 商品カテゴリーのためのモデル """

    product_type = models.CharField("商品タイプ名", max_length=20)
    type_code = models.CharField("タイプコード", max_length=2)


class Product(core_models.TimeStampedModel):

    """ 商品のモデルを定義する """

    name = models.CharField("商品名", max_length=50)
    category = models.ForeignKey(
        "Category", verbose_name="商品カテゴリー", on_delete=models.CASCADE
    )
    price = models.IntegerField("価格", default=0)
    description = models.TextField("詳細説明")
    is_active = models.BooleanField("販売中", null=False, default=True)
    product_code = models.CharField("商品番号", max_length=5)
