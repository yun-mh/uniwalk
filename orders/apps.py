from django.apps import AppConfig
import vinaigrette


# 対応状況のデータを翻訳するためのコード
class OrdersConfig(AppConfig):
    name = "orders"

    def ready(self):
        Ingredient = self.get_model("Step")
        vinaigrette.register(Ingredient, ["step_name"])

