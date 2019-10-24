from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ アドミンに商品を定義する """

    pass


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    """ アドミンに商品イメージを定義する """

    pass
