from django.db import models
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):

    """ レビューのモデルを定義する """

    # product = models.ForeignKey()
    # email = models.ForeignKey()
    title = models.CharField("タイトル", max_length=50)
    content = models.TextField("内容")
    score = models.IntegerField("評価")

    class Meta:
        verbose_name = "レビュー"
        verbose_name_plural = "レビュー"

    def __str__(self):
        return self.title
