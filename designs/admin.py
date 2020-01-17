from django.contrib import admin
from . import models

# Register your models here.
class ImageInline(admin.StackedInline):

    model = models.Image
    max_num = 1


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):

    """ アドミンに商品素材を定義する """

    list_display = (
        "name",
        "material_code",
    )

    list_per_page = 20


@admin.register(models.Design)
class DesignAdmin(admin.ModelAdmin):

    """ アドミンにデザインテーブルを定義する """

    inlines = (ImageInline,)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    """ あと削除 """
