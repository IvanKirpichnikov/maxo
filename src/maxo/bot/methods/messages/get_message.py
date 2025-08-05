from retejo.http.markers import UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.message import Message


class GetMessage(MaxoMethod[Message]):
    """
    Получить сообщение.

    Возвращает одно сообщение по его ID.

    Источник: https://dev.max.ru/docs-api/methods/GET/messages/-messageId-

    Args:
        message_id: ID сообщения (mid), чтобы получить одно сообщение в чате.

    """

    __url__ = "messages/{message_id}"
    __http_method__ = "get"

    message_id: UrlVar[str]
