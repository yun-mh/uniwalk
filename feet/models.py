from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile
from resizeimage import resizeimage

# イメージを自動ローテートするための関数(exif情報を持っているイメージの場合)
def rotate_image(path):
    # イメージからexifの情報を取得する
    try:
        image = Image.open(path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(image._getexif().items())
        # イメージを正しい方向にローテートする（回転方向は反時計回り）
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(path)
        image.close()
    # イメージにgetexifの情報が入っていない場合
    except (AttributeError, KeyError, IndexError):
        pass


class Footsize(core_models.TimeStampedModel):

    """ 足サイズのモデルを定義する """

    user = models.ForeignKey(
        "users.User",
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    length_left = models.DecimalField(_("足長(左)"), max_digits=3, decimal_places=0)
    length_right = models.DecimalField(_("足長(右)"), max_digits=3, decimal_places=0)
    width_left = models.DecimalField(_("足幅(左)"), max_digits=3, decimal_places=0)
    width_right = models.DecimalField(_("足幅(右)"), max_digits=3, decimal_places=0)

    def __str__(self):
        return str(self.user)


class FootImage(models.Model):

    """ 足イメージ """

    foot_left = models.ImageField(upload_to="feet")
    foot_right = models.ImageField(upload_to="feet")

    def save(self, *args, **kwargs):
        # exif情報を持っている場合イメージをローテートする
        rotate_image(self.foot_left)
        # 左足イメージのサイズ調整
        left_pil_image_obj = Image.open(self.foot_left)
        left_pil_image_obj = left_pil_image_obj.convert("RGB")
        left_new_image = resizeimage.resize_width(left_pil_image_obj, 500)
        left_new_image_io = BytesIO()
        left_new_image.save(left_new_image_io, format="JPEG")
        left_temp_name = self.foot_left.name
        self.foot_left.delete(save=False)
        self.foot_left.save(
            left_temp_name,
            content=ContentFile(left_new_image_io.getvalue()),
            save=False,
        )
        # exif情報を持っている場合イメージをローテートする
        rotate_image(self.foot_right)
        # 右足イメージのサイズ調整
        right_pil_image_obj = Image.open(self.foot_right)
        right_pil_image_obj = right_pil_image_obj.convert("RGB")
        right_new_image = resizeimage.resize_width(right_pil_image_obj, 500)
        right_new_image_io = BytesIO()
        right_new_image.save(right_new_image_io, format="JPEG")
        right_temp_name = self.foot_right.name
        self.foot_right.delete(save=False)
        self.foot_right.save(
            right_temp_name,
            content=ContentFile(right_new_image_io.getvalue()),
            save=False,
        )
        super(FootImage, self).save(*args, **kwargs)


class ProcessedFootImage(models.Model):

    """ 処理後の足イメージのためのモデル """

    foot_left = models.ImageField(upload_to="feet", blank=True, null=True)
    foot_right = models.ImageField(upload_to="feet", blank=True, null=True)
