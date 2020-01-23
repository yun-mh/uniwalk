from django.db import models
from core import models as core_models
from django.utils.translation import ugettext_lazy as _
from orders import models as order_models


def create_product_code():
    last_product = Product.objects.all().order_by("pk").last()
    if not last_product:
        return "0001"
    product_number = last_product.product_number
    product_int = int(product_number)
    no_width = 4
    new_product_int = product_int + 1
    formatted = (no_width - len(str(new_product_int))) * "0" + str(new_product_int)
    new_product_number = str(formatted)
    return new_product_number


def generate_path(self, filename):
    url = "product_templates/%s/%s" % (self.product.pk, filename)
    return url


class Template(models.Model):

    """ 商品の3Dテンプレートデータを取り扱う """

    product = models.ForeignKey(
        "Product",
        verbose_name=_("商品"),
        related_name="templates",
        on_delete=models.CASCADE,
    )
    shoelace_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    tongue_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    upper_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    midsole_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    outsole_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    liner_left = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    shoelace_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    tongue_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    upper_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    midsole_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    outsole_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )
    liner_right = models.FileField(
        upload_to=generate_path, null=True, blank=True, unique=True
    )


class Image(core_models.TimeStampedModel):

    """ 商品のイメージを管理するモデルを定義する """

    image = models.ImageField(_("イメージ"), upload_to="product_images")
    product = models.ForeignKey(
        "Product", verbose_name=_("商品"), related_name="images", on_delete=models.CASCADE
    )


class Category(core_models.TimeStampedModel):

    """ 商品カテゴリーのためのモデル """

    product_type = models.CharField(_("商品タイプ名"), max_length=20)
    type_code = models.CharField(_("タイプコード"), max_length=2)

    class Meta:
        verbose_name = _("カテゴリー")
        verbose_name_plural = _("カテゴリー")

    def __str__(self):
        return self.product_type


class Product(core_models.TimeStampedModel):

    """ 商品のモデルを定義する """

    name = models.CharField(_("商品名"), max_length=50)
    category = models.ForeignKey(
        "Category",
        verbose_name=_("商品カテゴリー"),
        related_name="product",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(_("価格"), decimal_places=0, max_digits=6)
    description = models.TextField(_("詳細説明"))
    is_active = models.BooleanField(_("販売中"), null=False, default=True)
    product_number = models.CharField(
        _("番号"), max_length=40, default=create_product_code, blank=True, null=True
    )
    product_code = models.CharField(_("商品番号"), max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rate
            return round(all_ratings / len(all_reviews), 2)
        return 0

    total_rating.short_description = _("評点")

    @property
    def first_image(self):
        try:
            (image,) = self.images.all()[:1]
            return image.image.url
        except ValueError:
            return None

    def get_next_four_images(self):
        images = self.images.all()[1:5]
        return images

    def get_orders_by_product(self):
        return len(order_models.OrderItem.objects.filter(product=self.pk))

    def save(self, *args, **kwargs):
        product_code = self.category.type_code + self.product_number
        self.product_code = product_code
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("商品")
        verbose_name_plural = _("商品")

