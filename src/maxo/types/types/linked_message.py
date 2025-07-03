from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.enums.message_link_type import MessageLinkType
from maxo.types.types.message_body import MessageBody
from maxo.types.types.user import User


class LinkedMessage(MaxoType):
    type: MessageLinkType
    sender: User
    chat_id: Omittable[int] = Omitted()
    message: MessageBody
