from django.contrib import admin
from . import models


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):

    """ アドミンにカートテーブルを定義する """

    pass
