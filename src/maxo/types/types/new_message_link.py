from maxo.types.base import MaxoType
from maxo.types.enums.message_link_type import MessageLinkType


class NewMessageLink(MaxoType):
    mid: str
    type: MessageLinkType
