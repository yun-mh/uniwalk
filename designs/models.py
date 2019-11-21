from django.db import models
from core import models as core_models

# Create your models here.
class Material(models.Model):

    """ 素材のモデルを定義する """

    name = models.CharField("", max_length=20)
    material_code = models.CharField("", max_length=2)


class Image(models.Model):

    """ カスタムデザインのイメージモデルを定義する """

    # design_id = models.ForeignKey()
    side_left = models.ImageField("側面(左)", upload_to="")
    side_right = models.ImageField("側面(右)", upload_to="")
    upper_left = models.ImageField("上面(左)", upload_to="")
    upper_right = models.ImageField("上面(右)", upload_to="")
    back_left = models.ImageField("後面(左)", upload_to="")
    back_right = models.ImageField("後面(右)", upload_to="")
    bottom_left = models.ImageField("下面(左)", upload_to="")
    bottom_right = models.ImageField("下面(右)", upload_to="")


class Design(core_models.TimeStampedModel):

    """ デザインのモデルを定義する """

    # user_id = models.ForeignKey()
    # product_id = models.ForeignKey()
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