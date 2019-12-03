from django.db import models
from core import models as core_models


class Image(core_models.TimeStampedModel):

    """ 商品のイメージを管理するモデルを定義する """

    image = models.ImageField("イメージ", upload_to="product_images")
    product = models.ForeignKey(
        "Product", verbose_name="商品", related_name="images", on_delete=models.CASCADE
    )


class Category(core_models.TimeStampedModel):

    """ 商品カテゴリーのためのモデル """

    product_type = models.CharField("商品タイプ名", max_length=20)
    type_code = models.CharField("タイプコード", max_length=2)

    def __str__(self):
        return self.product_type


class Product(core_models.TimeStampedModel):

    """ 商品のモデルを定義する """

    name = models.CharField("商品名", max_length=50)
    category = models.ForeignKey(
        "Category",
        verbose_name="商品カテゴリー",
        related_name="product",
        on_delete=models.CASCADE,
    )
    price = models.IntegerField("価格")
    description = models.TextField("詳細説明")
    is_active = models.BooleanField("販売中", null=False, default=True)
    product_code = models.CharField("商品番号", max_length=5)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_image(self):
        try:
            (image,) = self.images.all()[:1]
            return image.image.url
        except ValueError:
            return None

    def get_next_four_images(self):
        images = self.images.all()[1:5]
        return images
