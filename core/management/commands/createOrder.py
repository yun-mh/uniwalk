import random, time, datetime, math
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from products.models import Product
from orders.models import Order, Step
from users.models import User


# テストデータ用コマンドの作成
def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    print(stime)
    etime = time.mktime(time.strptime(end, format))
    print(etime)
    ptime = math.floor(stime + prop * (etime - stime))
    print(ptime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %H:%M:%S", prop)


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
        kanji_last = [
            "北口",
            "宮岡",
            "深堀",
            "本宮",
            "溝田",
            "茅野",
            "渡会",
            "河部",
            "関屋",
            "徳弘",
            "佐渡",
            "有友",
            "稲津",
            "笠見",
            "宗本",
            "池袋",
            "國司",
            "込宮",
            "羽沢",
            "磯谷",
            "蘇原",
            "南田",
            "吉間",
            "粟田",
            "時森",
        ]
        kanji_first = [
            "正宏",
            "克美",
            "達弥",
            "悠希",
            "真広",
            "保之",
            "昭人",
            "将人",
            "敏則",
            "康晃",
            "知一",
            "佑輝",
            "安雄",
            "信平",
            "昌輝",
            "直巳",
            "克英",
            "禎久",
            "勝平",
            "典行",
            "明英",
            "宏至",
            "泰晴",
            "光人",
            "博之",
        ]
        seeder = Seed.seeder()
        seeder.add_entity(
            Order,
            number,
            {
                "guest": None,
                "user": lambda x: random.choice(users),
                "step": lambda x: random.choice(steps),
                "amount": lambda x: random.choice(amounts),
                "last_name_orderer": lambda x: random.choice(kanji_last),
                "first_name_orderer": lambda x: random.choice(kanji_first),
                "order_date": random_date(
                    str(datetime.datetime(2020, 1, 1)),
                    str(datetime.datetime(2020, 3, 3)),
                    random.random(),
                ),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} orders created!"))
