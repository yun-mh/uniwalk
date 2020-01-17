from django.db import models
from core import models as core_models
from django.utils.translation import ugettext_lazy as _
from products import models as product_models


def create_custom_design_code():
    last_design = Design.objects.all().order_by("pk").last()
    if not last_design:
        return "00001"
    design_number = last_design.design_number
    design_int = int(design_number)
    no_width = 5
    new_design_int = design_int + 1
    formatted = (no_width - len(str(new_design_int))) * "0" + str(new_design_int)
    new_design_number = str(formatted)
    return new_design_number


class Material(core_models.TimeStampedModel):

    """ 素材のモデルを定義する """

    name = models.CharField(_("素材名"), max_length=20)
    file = models.FileField(_("素材画像"), upload_to="product_materials", blank=True)
    material_code = models.CharField(_("素材コード"), max_length=2)
    

class Image(models.Model):

    """ カスタムデザインのイメージモデルを定義する """

    design = models.ForeignKey(
        "Design",
        related_name="images",
        verbose_name="デザインid",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    side_left = models.ImageField(_("側面(左)"), upload_to="designs")
    side_right = models.ImageField(_("側面(右)"), upload_to="designs")
    upper_left = models.ImageField(_("上面(左)"), upload_to="designs")
    upper_right = models.ImageField(_("上面(右)"), upload_to="designs")
    back_left = models.ImageField(_("後面(左)"), upload_to="designs")
    back_right = models.ImageField(_("後面(右)"), upload_to="designs")
    bottom_left = models.ImageField(_("下面(左)"), upload_to="designs")
    bottom_right = models.ImageField(_("下面(右)"), upload_to="designs")


class Design(core_models.TimeStampedModel):

    """ デザインのモデルを定義する """

    user = models.ForeignKey(
        "users.User",
        related_name="design",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        "products.Product",
        related_name="design",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    outsole_color_left = models.CharField("アウトソール色(左)", max_length=7)
    # outsole_material_left = models.
    midsole_color_left = models.CharField("ミッドソール色(左)", max_length=7)
    # midsole_material_left = models.
    uppersole_color_left = models.CharField("アッパーソール色(左)", max_length=7)
    # uppersole_material_left = models.
    shoelace_color_left = models.CharField("シューレースホール色(左)", max_length=7)
    # shoelace_material_left = models.
    tongue_color_left = models.CharField("タン色(左)", max_length=7)
    # tongue_material_left = models.
    liner_color_left = models.CharField("ライナー色(左)", max_length=7)
    # liner_material_left = models.
    outsole_color_right = models.CharField("アウトソール色(右)", max_length=7)
    # outsole_material_right = models.
    midsole_color_right = models.CharField("ミッドソール色(右)", max_length=7)
    # midsole_material_right = models.
    uppersole_color_right = models.CharField("アッパーソール色(右)", max_length=7)
    # uppersole_material_right = models.
    shoelace_color_right = models.CharField("シューレースホール色(右)", max_length=7)
    # shoelace_material_right = models.
    tongue_color_right = models.CharField("タン色(右)", max_length=7)
    # tongue_material_right = models.
    liner_color_right = models.CharField("ライナー色(右)", max_length=7)
    # liner_material_right = models.
    design_number = models.CharField(
        _("番号"), max_length=40, default=create_custom_design_code, blank=True, null=True
    )
    customize_code = models.CharField("カスタマイズデザインコード", max_length=11)

    @property
    def first_image(self):
        try:
            (image,) = self.images.all()[:1]
            return image.side_left.url
        except ValueError:
            return None

    def get_key_four_images(self):
        images = self.objects.first().images
        return images

    def save(self, *args, **kwargs):
        product_code = self.product.product_code
        design_code = product_code + "C" + self.design_number
        self.customize_code = design_code
        super().save(*args, **kwargs)
