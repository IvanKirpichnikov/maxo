from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.message_link_type import MessageLinkType
from maxo.kerno.types.types.message_body import MessageBody
from maxo.kerno.types.types.user import User
from maxo.omit import Omittable, Omitted


class LinkedMessage(MaxoType):
    type: MessageLinkType
    sender: User
    chat_id: Omittable[int] = Omitted()
    message: MessageBody
