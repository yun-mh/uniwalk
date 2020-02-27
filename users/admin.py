from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from feet import models as feet_models
from orders import models as order_models
from reviews import models as review_models
from . import models


class ReviewInline(admin.TabularInline):

    model = review_models.Review
    verbose_name = _("レビュー")
    verbose_name_plural = _("レビュー")


class FootsizeInline(admin.TabularInline):

    model = feet_models.Footsize
    max_num = 1
    verbose_name = _("足サイズ")
    verbose_name_plural = _("足サイズ")


@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):

    fieldsets = ((_("ゲスト情報"), {"fields": ("email", "active",)},),)
    list_display = (
        "email",
        "created",
    )


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """ カスタムユーザーアドミン """

    fieldsets = (
        (
            _("会員情報"),
            {
                "fields": (
                    "email",
                    "password",
                    "last_name",
                    "first_name",
                    "last_name_kana",
                    "first_name_kana",
                    "gender",
                    "birthday",
                    "phone_number",
                    "postal_code",
                    "prefecture",
                    "address_city",
                    "address_detail",
                    "member_code",
                )
            },
        ),
        (
            _("認証・権限"),
            {
                "fields": (
                    "date_joined",
                    "last_login",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    inlines = (
        FootsizeInline,
        ReviewInline,
    )

    list_display = (
        "email",
        "get_fullname",
        "birthday",
        "gender",
        "member_code",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "email",
        "last_name",
        "first_name",
        "last_name_kana",
        "first_name_kana",
        "member_code",
    )

    list_filter = (
        "gender",
        "is_staff",
        "is_superuser",
    )

    list_per_page = 20

    def get_fullname(self, obj):
        return obj.last_name + obj.first_name

    get_fullname.short_description = _("会員名")

