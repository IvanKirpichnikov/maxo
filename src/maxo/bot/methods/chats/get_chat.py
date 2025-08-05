from retejo.http.markers import UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.chat import Chat


class GetChat(MaxoMethod[Chat]):
    """
    Получение информации о чате.

    Возвращает информацию о чате по его ID.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-

    Args:
        chat_id: ID запрашиваемого чата.

    """

    __url__ = "chats/{chat_id}"
    __http_method__ = "get"

    chat_id: UrlVar[int]
