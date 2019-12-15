from django.contrib import admin
from . import models


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):

    """ アドミンにカートテーブルを定義する """

    pass
