from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """ カスタムユーザーアドミン """

    fieldsets = (
        (
            "会員情報",
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
                )
            },
        ),
        (
            "認証・権限",
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

    list_display = (
        "get_fullname",
        "email",
        "birthday",
        "gender",
        "is_staff",
        "is_superuser",
    )

    def get_fullname(self, obj):
        return obj.last_name + obj.first_name

    get_fullname.short_description = "会員名"

