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
from weasyprint import HTML, CSS, default_url_fetcher
from . import models


class OrderItemInline(admin.TabularInline):

    model = models.OrderItem
    verbose_name = _("注文アイテム")
    verbose_name_plural = _("注文アイテム")


def make_step_new(self, request, queryset):
    step = models.Step.objects.get(step_code="T01")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 入金前に変更しました。" % message_bit)
make_step_new.short_description = "選択した注文を入金前に変更"

def make_step_payment_check(self, request, queryset):
    step = models.Step.objects.get(step_code="T02")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 決済処理中に変更しました。" % message_bit)
make_step_payment_check.short_description = "選択した注文を決済処理中に変更"

def make_step_payment_done(self, request, queryset):
    step = models.Step.objects.get(step_code="T03")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 決済確認済みに変更しました。" % message_bit)
make_step_payment_done.short_description = "選択した注文を決済確認済みに変更"

def make_step_dealing_with(self, request, queryset):
    step = models.Step.objects.get(step_code="T11")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 対応中に変更しました。" % message_bit)
make_step_dealing_with.short_description = "選択した注文を対応中に変更"

def make_step_shipping_done(self, request, queryset):
    step = models.Step.objects.get(step_code="T21")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 発送済みに変更しました。" % message_bit)
make_step_shipping_done.short_description = "選択した注文を発送済みに変更"

def make_step_cancel(self, request, queryset):
    step = models.Step.objects.get(step_code="T99")
    rows_updated = queryset.update(step=step)
    if rows_updated == 1:
        message_bit = "1件の注文の対応を"
    else:
        message_bit = "%s 注文の対応を" % rows_updated
    self.message_user(request, "%s 注文取消しに変更しました。" % message_bit)
make_step_cancel.short_description = "選択した注文を入金前に変更"


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """ アドミンに注文テーブルを定義する """

    change_form_template = "admin/order_changeform.html"

    fieldsets = (
        (
            _("注文情報"),
            {
                "fields": (
                    "order_code",
                    "order_date",
                    "user",
                    "guest",
                    "amount",
                    "payment",
                    # "stripe_charge_id",
                    "step",
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
        "amount",
        "step",
        "get_fullname_kana",
        "order_date",
        "bill",
        "receipt",
        "ordersheet",
        "orderspec",
        "invoice",
    )

    list_filter = (
        "step",
        "order_date",
    )

    list_per_page = 20

    actions = [make_step_new, make_step_payment_check, make_step_payment_done, make_step_dealing_with, make_step_shipping_done, make_step_cancel]

    inlines = (OrderItemInline,)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "bill/<int:pk>/", self.admin_site.admin_view(self.bill_pdf), name="bill",
            ),
            path(
                "receipt/<int:pk>/",
                self.admin_site.admin_view(self.receipt_pdf),
                name="receipt",
            ),
            path(
                "ordersheet/<int:pk>/",
                self.admin_site.admin_view(self.ordersheet_pdf),
                name="ordersheet",
            ),
            path(
                "orderspec/<int:pk>/",
                self.admin_site.admin_view(self.orderspec_pdf),
                name="orderspec",
            ),
            path(
                "invoice/<int:pk>/",
                self.admin_site.admin_view(self.invoice_pdf),
                name="invoice",
            ),
        ]
        return custom_urls + urls

    # 請求書
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

    # 領収書
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

    # 発注書
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

    # 製造仕様書
    def orderspec(self, obj):
        if obj.step.step_code == "T11":
            return format_html(
                '<a class="button" href="{}">仕様書</a>',
                reverse("admin:orderspec", args=[obj.pk]),
            )
        else:
            return ""

    orderspec.short_description = "仕様書"
    orderspec.allow_tags = True

    def orderspec_pdf(self, request, *args, **kwargs):
        order_pk = kwargs.get("pk")
        order = models.Order.objects.get(pk=order_pk)
        template = get_template("documents/specification.html")
        html = template.render({"order": order})
        response = HttpResponse(content_type="application/pdf")
        print(request.build_absolute_uri())
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
            response,
            stylesheets=[CSS(settings.STATICFILES_DIRS[0] + "/css/styles.css")],
        )
        return response

    # 納品書
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

    """ アドミンに対応テーブルを定義する """

    fieldsets = ((_("対応情報"), {"fields": ("step_code", "step_name",)},),)
    list_display = (
        "step_code",
        "step_name",
    )
