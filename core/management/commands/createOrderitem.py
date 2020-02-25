import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from products.models import Product
from orders.models import Order, OrderItem, Step
from designs.models import Material
from users.models import User


def randomColor():
    r = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (r(), r(), r())


class Command(BaseCommand):

    help = "This command creates orders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many orders you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        orders = Order.objects.all()
        products = Product.objects.all()
        materials = Material.objects.all()
        prices = [12000, 9000, 13000]
        seeder = Seed.seeder()
        seeder.add_entity(
            OrderItem,
            number,
            {
                "order": lambda x: random.choice(orders),
                "product": lambda x: random.choice(products),
                "quantity": lambda x: random.randint(1, 3),
                "price": lambda x: random.choice(prices),
                "outsole_color_left": randomColor(),
                "midsole_color_left": randomColor(),
                "uppersole_color_left": randomColor(),
                "shoelace_color_left": randomColor(),
                "tongue_color_left": randomColor(),
                "outsole_color_right": randomColor(),
                "midsole_color_right": randomColor(),
                "uppersole_color_right": randomColor(),
                "shoelace_color_right": randomColor(),
                "tongue_color_right": randomColor(),
                "outsole_material_left": random.choice(materials),
                "midsole_material_left": random.choice(materials),
                "uppersole_material_left": random.choice(materials),
                "shoelace_material_left": random.choice(materials),
                "tongue_material_left": random.choice(materials),
                "outsole_material_right": random.choice(materials),
                "midsole_material_right": random.choice(materials),
                "uppersole_material_right": random.choice(materials),
                "shoelace_material_right": random.choice(materials),
                "tongue_material_right": random.choice(materials),
                "length_left": lambda x: random.randint(190, 300),
                "length_right": lambda x: random.randint(190, 300),
                "width_left": lambda x: random.randint(70, 120),
                "width_right": lambda x: random.randint(70, 120),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} orders created!"))
