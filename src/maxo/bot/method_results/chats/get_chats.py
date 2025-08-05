from maxo.types.api.chat import Chat
from maxo.types.base import MaxoType


class GetChatsResult(MaxoType):
    """
    Результат метода GetChats.

    Args:
        chats: Список запрашиваемых чатов
        marker: Указатель на следующую страницу запрашиваемых чатов

    """

    chats: list[Chat]
    marker: int | None = None
