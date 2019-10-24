from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """ カスタムユーザーアドミン """

    list_display = ("get_fullname", "email", "birthday", "is_staff", "is_superuser")

    def get_fullname(self, obj):
        return obj.last_name + obj.first_name
