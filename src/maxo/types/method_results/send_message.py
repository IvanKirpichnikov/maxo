from maxo.types.base import MaxoType
from maxo.types.types.message import Message


class SendMessageResult(MaxoType):
    message: Message
