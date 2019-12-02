from django.db import models
from core import models as core_models

# Create your models here.
class Footsize(core_models.TimeStampedModel):

    """ 足サイズのモデルを定義する """

    user = models.ForeignKey(
        "users.User", verbose_name="ユーザー", on_delete=models.CASCADE
    )
    length_left = models.IntegerField("足長(左)")
    length_right = models.IntegerField("足長(右)")
    width_left = models.IntegerField("足幅(左)")
    width_right = models.IntegerField("足幅(右)")

    def __str__(self):
        return self.user
