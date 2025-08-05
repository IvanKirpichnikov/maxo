from retejo.http.markers import QueryParam

from maxo.bot.method_results.messages.delete_message import DeleteMessageResult
from maxo.bot.methods.base import MaxoMethod


class DeleteMessage(MaxoMethod[DeleteMessageResult]):
    """
    Удалить сообщение.

    Удаляет сообщение в диалоге или чате, если бот имеет разрешение на удаление сообщений.

    Источник: https://dev.max.ru/docs-api/methods/DELETE/messages

    Args:
        message_id: ID удаляемого сообщения.

    """

    __url__ = "messages"
    __http_method__ = "delete"

    message_id: QueryParam[str]
