from django.db import models
from core import models as core_models


class Step(models.Model):

    """ 注文の対応状況に関するモデルを定義する """

    step_code = models.CharField(max_length=3)
    step_name = models.CharField(max_length=20)


class Order(models.Model):

    """ 注文のモデルを定義する """

    PAYMENT_CARD = "P1"
    PAYMENT_TRANSFER = "P2"

    PAYMENT_CHOICES = ((PAYMENT_CARD, "クレジットカード"), (PAYMENT_TRANSFER, "振込"))

    user = models.ForeignKey(
        "users.User",
        related_name="order",
        verbose_name="ユーザー",
        on_delete=models.SET_NULL,
        null=True,
    )
    guest = models.ForeignKey(
        "users.Guest",
        related_name="order",
        verbose_name="ゲスト",
        on_delete=models.SET_NULL,
        null=True,
    )
    last_name_recipient = models.CharField("姓(ご請求書先)", max_length=30)
    first_name_recipient = models.CharField("名(ご請求書先)", max_length=30)
    last_name_recipient_kana = models.CharField("姓(ご請求書先,カナ)", max_length=30)
    first_name_recipient_kana = models.CharField("名(ご請求書先,カナ)", max_length=30)
    phone_number_recipient = models.CharField("電話番号(ご請求書先)", max_length=15)
    postal_code_recipient = models.CharField("郵便番号(ご請求書先)", max_length=7)
    prefecture_recipient = models.CharField("都道府県(ご請求書先)", max_length=2)
    address_city_recipient = models.CharField("市区町村(ご請求書先)", max_length=40)
    address_detail_recipient = models.CharField("建物名・部屋番号(ご請求書先)", max_length=40)
    last_name_orderer = models.CharField("姓(お届け先)", max_length=30)
    first_name_orderer = models.CharField("名(お届け先)", max_length=30)
    last_name_orderer_kana = models.CharField("姓(カナ, お届け先)", max_length=30)
    first_name_orderer_kana = models.CharField("名(カナ, お届け先)", max_length=30)
    phone_number_orderer = models.CharField("電話番号(お届け先)", max_length=15)
    postal_code_orderer = models.CharField("郵便番号(お届け先)", max_length=7)
    prefecture_orderer = models.CharField("都道府県(お届け先)", max_length=2)
    address_city_orderer = models.CharField("市区町村(お届け先)", max_length=40)
    address_detail_orderer = models.CharField("建物名・部屋番号(お届け先)", max_length=40)
    order_date = models.DateTimeField("注文日時", auto_now_add=True)
    payment = models.CharField("支払方法", max_length=2, choices=PAYMENT_CHOICES)
    # card_id = models.ForeignKey()
    # step = models.ForeignKey()
    amount = models.IntegerField("支払総額")


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
