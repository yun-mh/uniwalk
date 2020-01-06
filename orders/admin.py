from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


class OrderItemInline(admin.TabularInline):

    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """ アドミンに注文テーブルを定義する """

    fieldsets = (
        (
            _("注文情報"),
            {
                "fields": (
                    "order_code",
                    "order_date",
                    "user",
                    "guest",
                    "payment",
                    "stripe_charge_id",
                    "step",
                    "amount",
                )
            },
        ),
        (
            _("注文者情報"),
            {
                "fields": (
                    "last_name_orderer",
                    "first_name_orderer",
                    "last_name_orderer_kana",
                    "first_name_orderer_kana",
                    "phone_number_orderer",
                    "postal_code_orderer",
                    "prefecture_orderer",
                    "address_city_orderer",
                    "address_detail_orderer",
                )
            },
        ),
        (
            _("配送先情報"),
            {
                "fields": (
                    "last_name_recipient",
                    "first_name_recipient",
                    "last_name_recipient_kana",
                    "first_name_recipient_kana",
                    "phone_number_recipient",
                    "postal_code_recipient",
                    "prefecture_recipient",
                    "address_city_recipient",
                    "address_detail_recipient",
                )
            },
        ),
    )

    readonly_fields = ("order_date",)

    list_display = (
        "order_code",
        "step",
        "get_fullname",
        "get_fullname_kana",
        "order_date",
    )

    inlines = (OrderItemInline,)

    def get_fullname(self, obj):
        return obj.last_name_orderer + obj.first_name_orderer

    get_fullname.short_description = _("顧客名")

    def get_fullname_kana(self, obj):
        return obj.last_name_orderer_kana + obj.first_name_orderer_kana

    get_fullname_kana.short_description = _("顧客名(カナ)")


@admin.register(models.Step)
class StepAdmin(admin.ModelAdmin):

    """ アドミンに注文テーブルを定義する """

    list_display = (
        "step_code",
        "step_name",
    )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    """ アドミンに注文テーブルを定義する """

    pass
