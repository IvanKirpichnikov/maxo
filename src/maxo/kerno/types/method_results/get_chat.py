from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.chat import Chat
from maxo.omit import Omittable, Omitted


class GetChatResult(MaxoType):
    chats: list[Chat]
    marker: Omittable[int | None] = Omitted()
