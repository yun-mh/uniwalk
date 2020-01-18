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

    def __str__(self):
        return self.name + "(" + self.material_code + ")"


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
    front = models.ImageField(_("正面"), upload_to="designs")
    side = models.ImageField(_("側面"), upload_to="designs")
    up = models.ImageField(_("上面"), upload_to="designs")
    down = models.ImageField(_("下面"), upload_to="designs")


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
    outsole_material_left = models.ForeignKey(
        "Material",
        verbose_name=_("アウトソール素材(左)"),
        related_name="outsole_material_left",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    midsole_color_left = models.CharField("ミッドソール色(左)", max_length=7)
    midsole_material_left = models.ForeignKey(
        "Material",
        verbose_name=_("ミッドソール素材(左)"),
        related_name="midsole_material_left",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    uppersole_color_left = models.CharField("アッパーソール色(左)", max_length=7)
    uppersole_material_left = models.ForeignKey(
        "Material",
        verbose_name=_("アッパーソール素材(左)"),
        related_name="uppersole_material_left",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    shoelace_color_left = models.CharField("シューレース色(左)", max_length=7)
    shoelace_material_left = models.ForeignKey(
        "Material",
        verbose_name=_("シューレース素材(左)"),
        related_name="shoelace_material_left",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tongue_color_left = models.CharField("タン色(左)", max_length=7)
    tongue_material_left = models.ForeignKey(
        "Material",
        verbose_name=_("タン素材(左)"),
        related_name="tongue_material_left",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    outsole_color_right = models.CharField("アウトソール色(右)", max_length=7)
    outsole_material_right = models.ForeignKey(
        "Material",
        verbose_name=_("アウトソール素材(右)"),
        related_name="outsole_material_right",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    midsole_color_right = models.CharField("ミッドソール色(右)", max_length=7)
    midsole_material_right = models.ForeignKey(
        "Material",
        verbose_name=_("ミッドソール素材(右)"),
        related_name="midsole_material_right",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    uppersole_color_right = models.CharField("アッパーソール色(右)", max_length=7)
    uppersole_material_right = models.ForeignKey(
        "Material",
        verbose_name=_("アッパーソール素材(右)"),
        related_name="uppersole_material_right",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    shoelace_color_right = models.CharField("シューレース色(右)", max_length=7)
    shoelace_material_right = models.ForeignKey(
        "Material",
        verbose_name=_("シューレース素材(右)"),
        related_name="shoelace_material_right",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tongue_color_right = models.CharField("タン色(右)", max_length=7)
    tongue_material_right = models.ForeignKey(
        "Material",
        verbose_name=_("タン素材(右)"),
        related_name="tongue_material_right",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    design_number = models.CharField(
        _("番号"), max_length=40, default=create_custom_design_code, blank=True, null=True
    )
    customize_code = models.CharField("カスタマイズデザインコード", max_length=11)

    @property
    def first_image(self):
        try:
            (image,) = self.images.all()[:1]
            return image.front.url
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
