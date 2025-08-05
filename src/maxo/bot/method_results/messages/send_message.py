from maxo.types.api.message import Message
from maxo.types.base import MaxoType


class SendMessageResult(MaxoType):
    """
    Результат отправления сообщения.

    Args:
        message: Сообщение

    """

    message: Message
