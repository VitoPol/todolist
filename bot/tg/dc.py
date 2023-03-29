from dataclasses import dataclass
from typing import List

from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    username: str


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    # from_: MessageFrom = Field(..., alias='from')
    from_: MessageFrom
    chat: Chat
    date: int
    text: str


@dataclass
class MessageUpd(Message):
    language_code: str


@dataclass
class Entities:
    offset: int
    length: int
    type: str


@dataclass
class UpdateObj:
    update_id: int
    message: MessageUpd
    chat: Chat
    date: int
    text: str
    entities: List[Entities]


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
