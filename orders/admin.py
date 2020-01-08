import tempfile
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.template.loader import get_template
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
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
        "bill",
        "receipt",
        "ordersheet",
        "invoice",
    )

    inlines = (OrderItemInline,)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "invoice/<int:pk>",
                self.admin_site.admin_view(self.invoice_pdf),
                name="invoice",
            ),
            path(
                "bill/<int:pk>", self.admin_site.admin_view(self.bill_pdf), name="bill",
            ),
            path(
                "receipt/<int:pk>", self.admin_site.admin_view(self.receipt_pdf), name="receipt",
            ),
            path(
                "ordersheet/<int:pk>", self.admin_site.admin_view(self.ordersheet_pdf), name="ordersheet",
            ),
        ]
        return custom_urls + urls

    def bill(self, obj):
        if obj.step.step_code == "T01" or obj.step.step_code == "T02":
            return format_html(
                '<a class="button" href="{}">請求書</a>',
                reverse("admin:bill", args=[obj.pk]),
            )
        else:
            return ""

    bill.short_description = "請求書"
    bill.allow_tags = True

    def bill_pdf(self, request, *args, **kwargs):
        order_pk = kwargs.get("pk")
        order = models.Order.objects.get(pk=order_pk)

        template = get_template("documents/bill.html")
        html = template.render({"order": order})
        response = HttpResponse(content_type="application/pdf")
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
            response,
            stylesheets=[CSS(settings.STATICFILES_DIRS[0] + "/css/styles.css")],
        )
        return response

    def receipt(self, obj):
        if (
            obj.step.step_code == "T03"
            or obj.step.step_code == "T11"
            or obj.step.step_code == "T21"
        ):
            return format_html(
                '<a class="button" href="{}">領収書</a>',
                reverse("admin:receipt", args=[obj.pk]),
            )
        else:
            return ""

    receipt.short_description = "領収書"
    receipt.allow_tags = True
    
    def receipt_pdf(self, request, *args, **kwargs):
        order_pk = kwargs.get("pk")
        order = models.Order.objects.get(pk=order_pk)

        template = get_template("documents/receipt.html")
        html = template.render({"order": order})
        response = HttpResponse(content_type="application/pdf")
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
            response,
            stylesheets=[CSS(settings.STATICFILES_DIRS[0] + "/css/styles.css")],
        )
        return response

    def ordersheet(self, obj):
        if obj.step.step_code == "T11":
            return format_html(
                '<a class="button" href="{}">発注書</a>',
                reverse("admin:ordersheet", args=[obj.pk]),
            )
        else:
            return ""

    ordersheet.short_description = "発注書"
    ordersheet.allow_tags = True

    def ordersheet_pdf(self, request, *args, **kwargs):
        order_pk = kwargs.get("pk")
        order = models.Order.objects.get(pk=order_pk)

        template = get_template("documents/ordersheet.html")
        html = template.render({"order": order})
        response = HttpResponse(content_type="application/pdf")
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
            response,
            stylesheets=[CSS(settings.STATICFILES_DIRS[0] + "/css/styles.css")],
        )
        return response

    def invoice(self, obj):
        if obj.step.step_code == "T21":
            return format_html(
                '<a class="button" href="{}">納品書</a>',
                reverse("admin:invoice", args=[obj.pk]),
            )
        else:
            return ""

    invoice.short_description = "納品書"
    invoice.allow_tags = True

    def invoice_pdf(self, request, *args, **kwargs):
        order_pk = kwargs.get("pk")
        order = models.Order.objects.get(pk=order_pk)

        template = get_template("documents/invoice.html")
        html = template.render({"order": order})
        response = HttpResponse(content_type="application/pdf")
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
            response,
            stylesheets=[CSS(settings.STATICFILES_DIRS[0] + "/css/styles.css")],
        )
        return response

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
