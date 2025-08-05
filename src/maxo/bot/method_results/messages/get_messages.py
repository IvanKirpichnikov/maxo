from collections.abc import Sequence

from maxo.types.api.message import Message
from maxo.types.base import MaxoType


class GetMessagesResult(MaxoType):
    """
    Результат получения сообщений.

    Args:
        messages: Массив сообщений.

    """

    messages: Sequence[Message]
