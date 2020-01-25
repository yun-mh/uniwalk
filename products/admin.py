from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from . import models


class ImageInline(admin.TabularInline):

    model = models.Image
    max_num = 1


class TemplateInline(admin.StackedInline):

    model = models.Template
    max_num = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ アドミンに商品を定義する """

    change_list_template = "admin/change_list.html"
    inlines = (ImageInline, TemplateInline)
    fieldsets = (
        (
            _("商品情報"),
            {
                "fields": (
                    "name",
                    "category",
                    "price",
                    "description",
                    "is_active",
                    "product_code",
                )
            },
        ),
    )
    list_display = (
        "name",
        "get_thumbnail",
        "category",
        "product_code",
        "price",
        "total_rating",
    )
    search_fields = (
        "name",
        "product_code",
    )
    list_per_page = 20

    def get_thumbnail(self, obj):
        url = obj.first_image
        return mark_safe(f"<img width='50px' src='{url}'>")

    get_thumbnail.short_description = _("サムネイル")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):

    """ アドミンに商品カテゴリーを定義する """

    list_display = (
        "product_type",
        "type_code",
        "created",
    )

    list_per_page = 20
