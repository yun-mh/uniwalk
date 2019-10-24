from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """ 再利用可能なフィールドを各モデルに提供する """

    created = models.DateTimeField("登録日", auto_now_add=True)
    updated = models.DateTimeField("更新日", auto_now=True)

    class Meta:
        abstract = True
