from django.db import models
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):

    """ レビューのモデルを定義する """

    # product = models.ForeignKey()
    # email = models.ForeignKey()
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.IntegerField()
