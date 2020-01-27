from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class Footsize(core_models.TimeStampedModel):

    """ 足サイズのモデルを定義する """

    user = models.ForeignKey(
        "users.User",
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    length_left = models.DecimalField(_("足長(左)"), max_digits=4, decimal_places=1)
    length_right = models.DecimalField(_("足長(右)"), max_digits=4, decimal_places=1)
    width_left = models.DecimalField(_("足幅(左)"), max_digits=4, decimal_places=1)
    width_right = models.DecimalField(_("足幅(右)"), max_digits=4, decimal_places=1)

    def __str__(self):
        return str(self.user)


class FootImage(models.Model):

    length_left = models.FileField(upload_to="feet")
    length_right = models.FileField(upload_to="feet")
    width_left = models.FileField(upload_to="feet")
    width_right = models.FileField(upload_to="feet")
