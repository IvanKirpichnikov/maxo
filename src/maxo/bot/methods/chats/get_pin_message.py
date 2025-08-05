from retejo.http.markers import UrlVar

from maxo.bot.method_results.chats.get_pin_message import GetPinMessageResult
from maxo.bot.methods.base import MaxoMethod


class GetPinMessage(MaxoMethod[GetPinMessageResult]):
    """
    Получение закрепленного сообщения.

    Возвращает закрепленное сообщение в чате.

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-/pin

    Args:
        chat_id: ID чата.

    """

    __url__ = "chats/{chat_id}/pin"
    __http_method__ = "get"

    chat_id: UrlVar[int]
