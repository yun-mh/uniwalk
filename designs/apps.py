from django.apps import AppConfig
import vinaigrette


class DesignsConfig(AppConfig):
    name = "designs"

    def ready(self):
        Ingredient = self.get_model("Material")
        vinaigrette.register(Ingredient, ["name"])
