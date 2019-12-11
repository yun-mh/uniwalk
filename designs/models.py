from django.db import models
from core import models as core_models

# Create your models here.
class Material(models.Model):

    """ 素材のモデルを定義する """

    name = models.CharField("", max_length=20)
    material_code = models.CharField("", max_length=2)


class Image(models.Model):

    """ カスタムデザインのイメージモデルを定義する """

    design = models.ForeignKey(
        "Design", related_name="images", verbose_name="デザインid", on_delete=models.CASCADE
    )
    side_left = models.ImageField("側面(左)", upload_to="designs")
    side_right = models.ImageField("側面(右)", upload_to="designs")
    upper_left = models.ImageField("上面(左)", upload_to="designs")
    upper_right = models.ImageField("上面(右)", upload_to="designs")
    back_left = models.ImageField("後面(左)", upload_to="designs")
    back_right = models.ImageField("後面(右)", upload_to="designs")
    bottom_left = models.ImageField("下面(左)", upload_to="designs")
    bottom_right = models.ImageField("下面(右)", upload_to="designs")


class Design(core_models.TimeStampedModel):

    """ デザインのモデルを定義する """

    user = models.ForeignKey("users.User", related_name="design", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        "products.Product", related_name="design", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField("デザイン名", max_length=20)
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
    customize_code = models.CharField("カスタマイズデザインコード", max_length=11)

    def get_key_four_images(self):
        images = self.objects.first().images
        return images
