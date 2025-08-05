from retejo.http.markers import QueryParam, UrlVar

from maxo.bot.method_results.chats.get_chat_administrators import GetChatAdministratorsResult
from maxo.bot.methods.base import MaxoMethod
from maxo.omit import Omittable, Omitted


class GetChatAdministrators(MaxoMethod[GetChatAdministratorsResult]):
    """
    Получение списка администраторов чата.

    Возвращает всех администраторов чата. Бот должен быть администратором в запрашиваемом чате.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-/members/admins

    Args:
        chat_id: ID чата.
        marker: Указатель на следующую страницу данных.

    """

    __url__ = "chats/{chat_id}/members/admins"
    __http_method__ = "get"

    chat_id: UrlVar[int]

    marker: QueryParam[Omittable[int | None]] = Omitted()
