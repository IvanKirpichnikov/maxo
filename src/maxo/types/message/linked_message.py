from maxo.enums.message_link_type import MessageLinkType
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.message.message_body import MessageBody
from maxo.types.user.user import User

__all__ = ["LinkedMessage"]


class LinkedMessage(MaxoType):
    type: MessageLinkType
    sender: User
    chat_id: Omittable[int] = Omitted()
    message: MessageBody
