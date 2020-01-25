from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from reviews import models as review_models
from feet import models as feet_models
from . import models


class ReviewInline(admin.TabularInline):

    model = review_models.Review


class FootsizeInline(admin.TabularInline):

    model = feet_models.Footsize
    max_num = 1


@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):

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
                    "member_number",
                    "member_code",
                    "stripe_customer_id",
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
        ReviewInline,
        FootsizeInline,
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

    search_fields = ("email",)

    list_filter = (
        "gender",
        "is_staff",
        "is_superuser",
    )

    list_per_page = 20

    def get_fullname(self, obj):
        return obj.last_name + obj.first_name

    get_fullname.short_description = _("会員名")

