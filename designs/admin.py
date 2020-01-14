from django.contrib import admin
from . import models

# Register your models here.
class ImageInline(admin.TabularInline):

    model = models.Image


@admin.register(models.Design)
class DesignAdmin(admin.ModelAdmin):

    """ アドミンにデザインテーブルを定義する """

    inlines = (ImageInline,)
