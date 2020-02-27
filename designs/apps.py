from django.apps import AppConfig
import vinaigrette


# 素材データの翻訳のためのコード
class DesignsConfig(AppConfig):
    name = "designs"

    def ready(self):
        Ingredient = self.get_model("Material")
        vinaigrette.register(Ingredient, ["name"])
