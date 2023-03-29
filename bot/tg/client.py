import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        return GetUpdatesResponse(
            **(requests.get(self.get_url("getUpdates"), params={"offset": offset, "timeout": timeout}).json()))

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        return SendMessageResponse(
            **(requests.get(self.get_url("sendMessage"), params={"chat_id": chat_id, "text": text}).json()))
