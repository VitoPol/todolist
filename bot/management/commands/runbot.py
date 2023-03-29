from django.core.management.base import BaseCommand

from bot.tg.client import TgClient
from bot.models import TgUser
from goals.models import Goal, GoalCategory
from todolist.settings import BOT_TOKEN

from os import urandom


class Command(BaseCommand):
    tg_client = TgClient(BOT_TOKEN)
    state = "def"

    def fetch_tasks(self, item: dict, user: TgUser):
        gls = Goal.objects.filter(user=user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in gls]
            self.tg_client.send_message(item['message']["chat"]["id"], "\n".join(resp_msg))
        else:
            self.tg_client.send_message(item['message']["chat"]["id"], "У самурая нет цели, только путь")

    def fetch_goals_categories(self, item: dict, user: TgUser):
        chat_id = item['message']["chat"]["id"]
        categories = GoalCategory.objects.filter(user=user.user, is_deleted=False)
        if categories.count() > 0:
            resp_msg = [f"#{cat.id} {cat.title}" for cat in categories]
            self.tg_client.send_message(chat_id, "Выберете категорию\n" + "\n".join(resp_msg))
        else:
            self.tg_client.send_message(chat_id, "Категории отсутствуют")

    def create_task(self, item: dict, user):
        chat_id = item['message']["chat"]["id"]
        self.tg_client.send_message()

    def handle_verified(self, item: dict, user: TgUser):
        chat_id = item['message']["chat"]["id"]
        message = item["message"]["text"]
        match self.state:
            case 'def':
                match message:
                    case "/goals":
                        self.fetch_tasks(item, user)
                    case "/create":
                        self.fetch_goals_categories(item, user)
                        self.state = "choise cat"
                    case _:
                        self.tg_client.send_message(chat_id, "Не понял...")
            case "choise cat":
                if message == "/cancel":
                    self.state = "def"
                elif not GoalCategory.objects.filter(user=user.user, title=message, is_deleted=False).exists():
                    self.tg_client.send_message(chat_id, "Нет такой категории")

    def handle_main(self, item: dict):
        if not TgUser.objects.filter(tg_user_id=item['message']["from"]["id"]).exists():
            self.tg_client.send_message(item['message']["from"]["id"],
                                   f"Привет, '{item['message']['from']['username']}'!")
            TgUser.objects.create(tg_chat_id=item['message']["chat"]["id"], tg_user_id=item['message']["from"]["id"])
        else:
            user = TgUser.objects.get(tg_user_id=item['message']["from"]["id"])
            if user.user is None:
                code = urandom(10).hex()
                user.verification_code = code
                user.save()
                self.tg_client.send_message(item['message']["chat"]["id"], f"Ваш код верификации: {code}")
            else:
                self.handle_verified(item, user)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item['update_id'] + 1
                self.handle_main(item)

