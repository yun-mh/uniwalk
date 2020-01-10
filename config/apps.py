from django.contrib.admin.apps import AdminConfig


class ConfigAdminConfig(AdminConfig):
    default_site = "config.admin.ConfigAdminSite"

