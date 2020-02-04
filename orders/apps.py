from django.apps import AppConfig
import vinaigrette


class OrdersConfig(AppConfig):
    name = "orders"

    def ready(self):
        # Import the model requiring translation
        Ingredient = self.get_model("Step")

        # Register fields to translate
        vinaigrette.register(Ingredient, ["step_name"])

