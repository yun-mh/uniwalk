from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Footsize)
class FootsizeAdmin(admin.ModelAdmin):

    """ アドミンに足サイズテーブルを定義する """

    pass