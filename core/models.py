from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """ 再利用可能なフィールドを各モデルに提供する """

    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        abstract = True
