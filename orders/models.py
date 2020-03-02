import random, string
from datetime import datetime, date
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from core import models as core_models
from core.models import JPPrefectureField


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

    step_code = models.CharField(_("対応コード"), max_length=3)
    step_name = models.CharField(_("対応名"), max_length=20)

    def __str__(self):
        return self.step_name

    class Meta:
        ordering = ("step_code",)
        verbose_name = _("対応")
        verbose_name_plural = _("対応")


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
    last_name_recipient_kana = models.CharField(
        _("姓(ご請求書先,カナ)"),
        max_length=30,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    first_name_recipient_kana = models.CharField(
        _("名(ご請求書先,カナ)"),
        max_length=30,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    phone_number_recipient = PhoneNumberField(_("電話番号(ご請求書先)"), max_length=15)
    postal_code_recipient = models.CharField(_("郵便番号(ご請求書先)"), max_length=7)
    prefecture_recipient = JPPrefectureField(_("都道府県(ご請求書先)"), max_length=2)
    address_city_recipient = models.CharField(_("市区町村(ご請求書先)"), max_length=40)
    address_detail_recipient = models.CharField(_("建物名・部屋番号(ご請求書先)"), max_length=40)
    last_name_orderer = models.CharField(_("姓(お届け先)"), max_length=30)
    first_name_orderer = models.CharField(
        _("名(お届け先)"), max_length=30, null=True, blank=True
    )
    last_name_orderer_kana = models.CharField(
        _("姓(カナ, お届け先)"),
        max_length=30,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    first_name_orderer_kana = models.CharField(
        _("名(カナ, お届け先)"),
        max_length=30,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex="[ア-ンー]", message=_("全角カタカナで入力してください。"), code="invalid",
            ),
        ],
    )
    phone_number_orderer = PhoneNumberField(
        _("電話番号(お届け先)"), max_length=15, null=True, blank=True
    )
    postal_code_orderer = models.CharField(
        _("郵便番号(お届け先)"), max_length=7, null=True, blank=True
    )
    prefecture_orderer = JPPrefectureField(
        _("都道府県(お届け先)"), max_length=2, null=True, blank=True
    )
    address_city_orderer = models.CharField(
        _("市区町村(お届け先)"), max_length=40, null=True, blank=True
    )
    address_detail_orderer = models.CharField(
        _("建物名・部屋番号(お届け先)"), max_length=40, null=True, blank=True
    )
    order_date = models.DateTimeField(_("注文日時"), auto_now_add=True)
    payment = models.CharField(_("支払方法"), max_length=2, choices=PAYMENT_CHOICES)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    step = models.ForeignKey(
        "Step",
        related_name="order",
        verbose_name=_("対応状況"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    amount = models.DecimalField(_("支払総額"), decimal_places=0, max_digits=10)
    order_number = models.CharField(
        max_length=40, default=create_order_number, blank=True, null=True
    )
    order_code = models.CharField(_("注文番号"), max_length=40, blank=True, null=True)

    class Meta:
        ordering = ("-order_date",)
        verbose_name = _("注文")
        verbose_name_plural = _("注文")

    def show_first_one(self):
        try:
            (order_item,) = self.order_items.all()[:1]
            return order_item.product
        except ValueError:
            return None

    def count_items_all(self):
        count = 0
        for order_item in self.order_items.all():
            count += order_item.quantity
        return count

    def count_items_except_one(self):
        return self.order_items.all().count() - 1


# モデルにデータを保存した後に注文コードを付与し再保存する
@receiver(post_save, sender=Order)
def set_order_code(sender, instance, created, **kwargs):
    if created:
        order_date = instance.order_date
        try:
            date_string = order_date.strftime("%y%m")
        except:
            temp = order_date.split("-")
            date_string = temp[0] + temp[1]
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
    order = models.ForeignKey(
        "Order",
        verbose_name=_("注文アイテム"),
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "products.Product",
        verbose_name=_("商品"),
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(_("数量"))
    price = models.DecimalField(_("単価"), decimal_places=0, max_digits=6)
    front = models.ImageField(_("正面"), upload_to="orders")
    side = models.ImageField(_("側面"), upload_to="orders")
    up = models.ImageField(_("上面"), upload_to="orders")
    down = models.ImageField(_("下面"), upload_to="orders")
    outsole_color_left = models.CharField("アウトソール色(左)", max_length=7)
    outsole_material_left = models.CharField("アウトソール素材(左)", max_length=20)
    midsole_color_left = models.CharField("ミッドソール色(左)", max_length=7)
    midsole_material_left = models.CharField("ミッドソール素材(左)", max_length=20)
    uppersole_color_left = models.CharField("アッパーソール色(左)", max_length=7)
    uppersole_material_left = models.CharField("アッパーソール素材(左)", max_length=20)
    shoelace_color_left = models.CharField("シューレース色(左)", max_length=7)
    shoelace_material_left = models.CharField("シューレース素材(左)", max_length=20)
    tongue_color_left = models.CharField("タン色(左)", max_length=7)
    tongue_material_left = models.CharField("タン素材(左)", max_length=20)
    outsole_color_right = models.CharField("アウトソール色(右)", max_length=7)
    outsole_material_right = models.CharField("アウトソール素材(右)", max_length=20)
    midsole_color_right = models.CharField("ミッドソール色(右)", max_length=7)
    midsole_material_right = models.CharField("ミッドソール素材(右)", max_length=20)
    uppersole_color_right = models.CharField("アッパーソール色(右)", max_length=7)
    uppersole_material_right = models.CharField("アッパーソール素材(右)", max_length=20)
    shoelace_color_right = models.CharField("シューレース色(右)", max_length=7)
    shoelace_material_right = models.CharField("シューレース素材(右)", max_length=20)
    tongue_color_right = models.CharField("タン色(右)", max_length=7)
    tongue_material_right = models.CharField("タン素材(右)", max_length=20)
    customize_code = models.CharField(_("カスタマイズデザインコード"), max_length=11)
    length_left = models.DecimalField(_("足長(左)"), max_digits=3, decimal_places=0)
    length_right = models.DecimalField(_("足長(右)"), max_digits=3, decimal_places=0)
    width_left = models.DecimalField(_("足幅(左)"), max_digits=3, decimal_places=0)
    width_right = models.DecimalField(_("足幅(右)"), max_digits=3, decimal_places=0)

    def sub_total(self):
        return self.quantity * self.price

