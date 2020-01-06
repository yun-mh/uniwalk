from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from . import models


class ImageInline(admin.TabularInline):

    model = models.Image


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ アドミンに商品を定義する """

    inlines = (ImageInline,)
    list_display = (
        "name",
        "get_thumbnail",
        "category",
        "product_code",
        "price",
        "total_rating",
    )

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
