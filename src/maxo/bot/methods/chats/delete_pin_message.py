from retejo.http.markers import UrlVar

from maxo.bot.method_results.chats.delete_pin_message import DeletePinMessageResult
from maxo.bot.methods.base import MaxoMethod


class DeletePinMessage(MaxoMethod[DeletePinMessageResult]):
    """
    Удаление закрепленного сообщения.

    Удаляет закрепленное сообщение в чате.

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/pin

    Args:
        chat_id: ID чата, у которого нужно удалить закрепленное сообщение.

    """

    __url__ = "chats/{chat_id}/pin"
    __http_method__ = "delete"

    chat_id: UrlVar[int]
