import time
import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from products.models import Product
from users.models import User


# テストデータ用コマンドの作成
class Command(BaseCommand):

    help = "This command creates reviews."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many reviews you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        users = User.objects.all()
        products = Product.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Review,
            number,
            {
                "product": lambda x: random.choice(products),
                "user": lambda x: random.choice(users),
                "rate": lambda x: random.randint(4, 5),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!"))
