from retejo.http.markers import Body, UrlVar

from maxo.bot.method_results.chats.pin_message import PinMessageResult
from maxo.bot.methods.base import MaxoMethod
from maxo.omit import Omittable


class PinMessage(MaxoMethod[PinMessageResult]):
    """
    Закрепление сообщения.

    Закрепляет сообщение в чате.

    Источник: https://dev.max.ru/docs-api/methods/PUT/chats/-chatId-/pin

    Args:
        chat_id: ID чата, где должно быть закреплено сообщение.
        message_id: ID(mid) сообщения, которое нужно закрепить.
        notify: Если true, участники получат уведомление с системным сообщением о закреплении.

    """

    __url__ = "chats/{chat_id}/pin"
    __http_method__ = "put"

    chat_id: UrlVar[int]

    message_id: Body[str]
    notify: Body[Omittable[bool]] = True
