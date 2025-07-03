from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.message_link_type import MessageLinkType


class NewMessageLink(MaxoType):
    mid: str
    type: MessageLinkType
