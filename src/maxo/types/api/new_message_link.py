from maxo.types.base import MaxoType
from maxo.types.enums.message_link_type import MessageLinkType


class NewMessageLink(MaxoType):
    """
    Ссылка на новое сообщение.

    Args:
        mid: ID сообщения исходного сообщения.
        type: Тип ссылки сообщения.

    """

    mid: str
    type: MessageLinkType
