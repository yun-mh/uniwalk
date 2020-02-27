from django.contrib import admin
from . import models


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):

    """ アドミンにカードテーブルを定義する """

    pass
