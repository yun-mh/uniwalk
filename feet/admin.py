from django.contrib import admin
from . import models


@admin.register(models.Footsize)
class FootsizeAdmin(admin.ModelAdmin):

    """ アドミンに足サイズテーブルを定義する """

    pass


@admin.register(models.FootImage)
class FootImageAdmin(admin.ModelAdmin):

    """ アドミンに足サイズテーブルを定義する """

    pass

@admin.register(models.ProcessedFootImage)
class ProcessedFootImageAdmin(admin.ModelAdmin):

    """ 削除する！ """

    pass
