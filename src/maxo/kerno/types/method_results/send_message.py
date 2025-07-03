from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.message import Message


class SendMessageResult(MaxoType):
    message: Message
