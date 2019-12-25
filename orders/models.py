import random, string
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models


def create_order_number():
    last_order = Order.objects.all().order_by("pk").last()
    if not last_order:
        return "0001"
    order_number = last_order.order_number
    order_int = int(order_number)
    no_width = 4
    new_order_int = order_int + 1
    if not new_order_int == 10000:
        formatted = (no_width - len(str(new_order_int))) * "0" + str(new_order_int)
    else:
        formatted = "0001"
    new_order_number = str(formatted)
    return new_order_number


class Step(models.Model):

    """ 注文の対応状況に関するモデルを定義する """

    step_code = models.CharField(max_length=3)
    step_name = models.CharField(max_length=20)


class Order(models.Model):

    """ 注文のモデルを定義する """

    PAYMENT_CARD = "P1"
    PAYMENT_TRANSFER = "P2"

    PAYMENT_CHOICES = ((PAYMENT_CARD, _("クレジットカード")), (PAYMENT_TRANSFER, _("振込")))

    user = models.ForeignKey(
        "users.User",
        related_name="order",
        verbose_name=_("ユーザー"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    guest = models.ForeignKey(
        "users.Guest",
        related_name="order",
        verbose_name=_("ゲスト"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    last_name_recipient = models.CharField(_("姓(ご請求書先)"), max_length=30)
    first_name_recipient = models.CharField(_("名(ご請求書先)"), max_length=30)
    last_name_recipient_kana = models.CharField(_("姓(ご請求書先,カナ)"), max_length=30)
    first_name_recipient_kana = models.CharField(_("名(ご請求書先,カナ)"), max_length=30)
    phone_number_recipient = PhoneNumberField(_("電話番号(ご請求書先)"), max_length=15)
    postal_code_recipient = models.CharField(_("郵便番号(ご請求書先)"), max_length=7)
    prefecture_recipient = models.CharField(_("都道府県(ご請求書先)"), max_length=2)
    address_city_recipient = models.CharField(_("市区町村(ご請求書先)"), max_length=40)
    address_detail_recipient = models.CharField(_("建物名・部屋番号(ご請求書先)"), max_length=40)
    last_name_orderer = models.CharField(_("姓(お届け先)"), max_length=30)
    first_name_orderer = models.CharField(_("名(お届け先)"), max_length=30)
    last_name_orderer_kana = models.CharField(_("姓(カナ, お届け先)"), max_length=30)
    first_name_orderer_kana = models.CharField(_("名(カナ, お届け先)"), max_length=30)
    phone_number_orderer = PhoneNumberField(_("電話番号(お届け先)"), max_length=15)
    postal_code_orderer = models.CharField(_("郵便番号(お届け先)"), max_length=7)
    prefecture_orderer = models.CharField(_("都道府県(お届け先)"), max_length=2)
    address_city_orderer = models.CharField(_("市区町村(お届け先)"), max_length=40)
    address_detail_orderer = models.CharField(_("建物名・部屋番号(お届け先)"), max_length=40)
    order_date = models.DateTimeField(_("注文日時"), auto_now_add=True)
    payment = models.CharField(_("支払方法"), max_length=2, choices=PAYMENT_CHOICES)
    # card_id = models.ForeignKey()
    # step = models.ForeignKey()
    amount = models.IntegerField(_("支払総額"))
    order_number = models.CharField(
        max_length=40, default=create_order_number, blank=True, null=True
    )
    order_code = models.CharField(_("注文番号"), max_length=40, blank=True, null=True)


@receiver(post_save, sender=Order)
def set_order_code(sender, instance, created, **kwargs):
    if created:
        order_date = instance.order_date
        date_string = order_date.strftime("%y%m")
        if instance.user:
            instance.order_code = (
                date_string + instance.user.member_code + instance.order_number
            )
            instance.save()
        else:
            string_pool = string.ascii_uppercase
            char1 = random.choice(string_pool)
            char2 = random.choice(string_pool)
            instance.order_code = (
                date_string + "UWGUEST" + char1 + char2 + instance.order_number
            )
            instance.save()


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
