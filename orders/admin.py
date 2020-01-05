from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    """ アドミンに注文テーブルを定義する """

    list_display = (
        "last_name_recipient",
        "first_name_recipient",
        "order_date",
        "order_number",
        "order_code",
    )


@admin.register(models.Step)
class StepAdmin(admin.ModelAdmin):
    """ アドミンに注文テーブルを定義する """

    list_display = (
        "step_code",
        "step_name",
    )
