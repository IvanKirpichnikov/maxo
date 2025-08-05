from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ChatKeyboardButton(MaxoType):
    text: str
    chat_title: str
    chat_description: Omittable[str | None] = Omitted()
    start_payload: Omittable[str | None] = Omitted()
    uuid: Omittable[int | None] = Omitted()
