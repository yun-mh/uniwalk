from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models

# Create your models here.
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
