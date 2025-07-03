from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.enums.intent import IntentType


class CallbackKeyboardButton(MaxoType):
    text: str
    payload: str
    intent: IntentType = IntentType.DEFAULT


class ChatKeyboardButton(MaxoType):
    text: str
    chat_title: str
    chat_description: Omittable[str | None] = Omitted()
    start_payload: Omittable[str | None] = Omitted()
    uuid: Omittable[int | None] = Omitted()


class LinkKeyboardButton(MaxoType):
    text: str
    url: str


class RequestContactKeyboardButton(MaxoType):
    text: str


class RequestGeoLocationKeyboardButton(MaxoType):
    text: str
    quick: Omittable[bool] = Omitted()


KeyboardButtons = (
    CallbackKeyboardButton
    | LinkKeyboardButton
    | RequestGeoLocationKeyboardButton
    | RequestContactKeyboardButton
    | ChatKeyboardButton
)
Keyboard = Sequence[Sequence[KeyboardButtons]]
