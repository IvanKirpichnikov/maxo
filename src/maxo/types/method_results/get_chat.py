from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.chat import Chat

__all__ = ["GetChatResult"]


class GetChatResult(MaxoType):
    chats: list[Chat]
    marker: Omittable[int | None] = Omitted()
