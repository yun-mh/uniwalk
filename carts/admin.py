from django.contrib import admin
from . import models


class CartItemInline(admin.TabularInline):

    model = models.CartItem


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):

    """ アドミンにカートテーブルを定義する """

    inlines = (CartItemInline,)


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):

    """ アドミンにカートテーブルを定義する """

    pass
