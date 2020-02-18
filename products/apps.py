from django.apps import AppConfig
import vinaigrette


class ProductsConfig(AppConfig):
    name = "products"

    def ready(self):
        Ingredient = self.get_model("Product")
        vinaigrette.register(Ingredient, ["description"])
