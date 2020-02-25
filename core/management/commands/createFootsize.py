import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from feet.models import Footsize


class Command(BaseCommand):

    help = "This command creates footsizes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many footsizes you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        users = User.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            Footsize,
            number,
            {
                "user": lambda x: random.choice(users),
                "length_left": lambda x: random.randint(190, 300),
                "length_right": lambda x: random.randint(190, 300),
                "width_left": lambda x: random.randint(70, 120),
                "width_right": lambda x: random.randint(70, 120),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} footsizes created!"))
