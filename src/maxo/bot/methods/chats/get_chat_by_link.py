from retejo.http.markers import UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.chat import Chat


class GetChatByLink(MaxoMethod[Chat]):
    """
    Получение чата по ссылке.

    Возвращает информацию о чате по его публичной ссылке,
    либо информацию о диалоге с пользователем по его username.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatLink-

    Args:
        url: Публичная ссылка на чат или username пользователя.

    """

    __url__ = "chats/{url}"
    __http_method__ = "get"

    url: UrlVar[str]
