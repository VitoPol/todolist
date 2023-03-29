from django.core.management.base import BaseCommand

from bot.tg.client import TgClient
from bot.models import TgUser
from todolist.settings import BOT_TOKEN

from os import urandom


class Command(BaseCommand):
    tg_client = TgClient(BOT_TOKEN)

    def handle_main(self, item: dict):
        if not TgUser.objects.filter(tg_user_id=item['message']["from"]["id"]).exists():
            self.tg_client.send_message(item['message']["from"]["id"],
                                   f"Привет, '{item['message']['from']['username']}'!")
            TgUser.objects.create(tg_chat_id=item['message']["chat"]["id"], tg_user_id=item['message']["from"]["id"])
        else:
            code = urandom(10).hex()
            user = TgUser.objects.get(tg_user_id=item['message']["from"]["id"])
            user.verification_code = code
            user.save()
            self.tg_client.send_message(item['message']["chat"]["id"], f"Ваш код верификации: {code}")

    def handle(self, *args, **options):
        offset = 0
        # tg_client = TgClient("5744181406:AAEduEORLSPGWGq7B2GHpszzPpgeCey6dM8")
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item['update_id'] + 1
                self.handle_main(item)
                # tg_client.send_message(item['message']["chat"]["id"], f"Все говорят '{item['message']['text']}', а ты купи слона")

