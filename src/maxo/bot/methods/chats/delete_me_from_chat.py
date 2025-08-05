from retejo.http.markers import UrlVar

from maxo.bot.method_results.chats.delete_me_from_chat import DeleteMeFromChatResult
from maxo.bot.methods.base import MaxoMethod


class DeleteMeFromChat(MaxoMethod[DeleteMeFromChatResult]):
    """
    Удаление бота из чата.

    Удаляет бота из участников чата.

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/members/me

    Args:
        chat_id: ID чата.

    """

    __url__ = "chats/{chat_id}/members/me"
    __http_method__ = "delete"

    chat_id: UrlVar[int]
