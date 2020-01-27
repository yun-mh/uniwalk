from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models


class ImageInline(admin.StackedInline):

    model = models.Image
    max_num = 1


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):

    """ アドミンに商品素材を定義する """

    fieldsets = ((_("素材情報"), {"fields": ("name", "material_code", "file")},),)
    list_display = (
        "name",
        "material_code",
    )
    list_per_page = 20


@admin.register(models.Design)
class DesignAdmin(admin.ModelAdmin):

    """ アドミンにデザインテーブルを定義する """

    fieldsets = (
        (
            _("デザイン情報"), 
            {
                "fields": (
                    "customize_code", 
                    "product", 
                    "user", 
                    "likes"
                )
            },
        ),
        (
            _("デザイン詳細"), 
            {
                "fields": (
                    "outsole_color_left",
                    "outsole_material_left",
                    "midsole_color_left",
                    "midsole_material_left",
                    "uppersole_color_left",
                    "uppersole_material_left",
                    "shoelace_color_left",
                    "shoelace_material_left",
                    "tongue_color_left",
                    "tongue_material_left",
                    "outsole_color_right",
                    "outsole_material_right",
                    "midsole_color_right",
                    "midsole_material_right",
                    "uppersole_color_right",
                    "uppersole_material_right",
                    "shoelace_color_right",
                    "shoelace_material_right",
                    "tongue_color_right",
                    "tongue_material_right",
                )
            },
        )
    )
    list_display = (
        "customize_code",
        "created",
    )
    inlines = (ImageInline,)
