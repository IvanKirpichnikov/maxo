from enum import StrEnum


class MessageLinkType(StrEnum):
    """
    Тип связанного сообщения.

    Attributes:
        REPLY: Ответное сообщение.
        FORWARD: Пересланное сообщение.

    """

    REPLY = "reply"
    FORWARD = "forward"
