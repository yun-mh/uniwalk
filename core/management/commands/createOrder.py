import random, time
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from products.models import Product
from orders.models import Order, Step
from users.models import User


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %H:%M", prop)


class Command(BaseCommand):

    help = "This command creates orders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many orders you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        users = User.objects.all()
        steps = Step.objects.all()
        amounts = [12000, 9000, 13000, 21000]
        seeder = Seed.seeder()
        seeder.add_entity(
            Order,
            number,
            {
                "guest": None,
                "user": lambda x: random.choice(users),
                "step": lambda x: random.choice(steps),
                "amount": lambda x: random.choice(amounts),
                # "order_date": random_date(
                #     "2019-01-01 06:00", "2019-12-25 06:00", random.random(),
                # ),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} orders created!"))
