from maxo.enums.message_link_type import MessageLinkType
from maxo.types.base import MaxoType

__all__ = ["NewMessageLink"]


class NewMessageLink(MaxoType):
    mid: str
    type: MessageLinkType
