from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Footsize)
class FootsizeAdmin(admin.ModelAdmin):

    """ アドミンに商品を定義する """

    pass