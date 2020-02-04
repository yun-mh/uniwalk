from django.apps import AppConfig
import vinaigrette


class OrdersConfig(AppConfig):
    name = "orders"

    def ready(self):
        Ingredient = self.get_model("Step")
        vinaigrette.register(Ingredient, ["step_name"])

