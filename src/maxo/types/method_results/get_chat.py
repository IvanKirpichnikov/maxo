from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.types.chat import Chat


class GetChatResult(MaxoType):
    chats: list[Chat]
    marker: Omittable[int | None] = Omitted()
