from retejo.http.markers import UrlVar

from maxo.bot.method_results.chats.delete_chat import DeleteChatResult
from maxo.bot.methods.base import MaxoMethod


class DeleteChat(MaxoMethod[DeleteChatResult]):
    """
    Удалить чат.

    Удаляет чат для всех участников.

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-

    Args:
        chat_id: int

    """

    __url__ = "chats/{chat_id}"
    __http_method__ = "delete"

    chat_id: UrlVar[int]
