from django.db import models

# Create your models here.
class Card(models.Model):

    """ カードのモデルを定義する """

    # user_id = models.ForeignKey()
    last_name = models.CharField("姓", max_length=20)
    first_name = models.CharField("名", max_length=20)
    card_number = models.CharField("カード番号", max_length=16)
    expiration_month = models.CharField("有効期限(月)", max_length=2)
    expiration_year = models.CharField("有効期限(年)", max_length=2)