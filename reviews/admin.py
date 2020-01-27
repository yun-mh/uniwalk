from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ アドミンにレビューを定義する """

    fieldsets = ((_("レビュー情報"), {"fields": ("title", "user", "product", "text", "rate",)},),)
    list_display = (
        "title",
        "user",
        "product",
        "rate",
        "created",
        "updated",
    )
