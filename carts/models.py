from django.db import models
from core import models as core_models
from users import models as user_models


class Cart(core_models.TimeStampedModel):

    """ カートのモデルを定義する """

    user = models.ForeignKey(
        user_models.User, null=True, blank=True, on_delete=models.CASCADE
    )
    # products    = models.ManyToManyField(Product, blank=True)
    subtotal = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

