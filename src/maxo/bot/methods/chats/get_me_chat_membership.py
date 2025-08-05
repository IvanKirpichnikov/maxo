from retejo.http.markers import UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.chat_membership import ChatMembership


class GetMeChatMembership(MaxoMethod[ChatMembership]):
    """
    Получение информации о членстве в чате.

    Возвращает информацию о членстве текущего бота в чате.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-/members/me

    Args:
        chat_id: ID чата.

    """

    __url__ = "/chats/{chat_id}/members/me"
    __http_method__ = "get"

    chat_id: UrlVar[int]
