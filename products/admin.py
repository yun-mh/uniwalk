from django.contrib import admin
from . import models

# Register your models here.
class ImageInline(admin.TabularInline):

    model = models.Image


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ アドミンに商品を定義する """

    inlines = (ImageInline,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):

    """ アドミンに商品カテゴリーを定義する """

    list_display = (
        "product_type",
        "type_code",
        "created",
    )
