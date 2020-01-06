from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ アドミンにレビューを定義する """

    list_display = (
        "title",
        "user",
        "product",
        "rate",
        "created",
        "updated",
    )
