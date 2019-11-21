from django.db import models
from core import models as core_models

# Create your models here.
class Footsize(core_models.TimeStampedModel):

    """ 足サイズのモデルを定義する """

    # user_id = models.ForeignKey()
    length_left = models.IntegerField()
    length_right = models.IntegerField()
    width_left = models.IntegerField()
    width_right = models.IntegerField()
