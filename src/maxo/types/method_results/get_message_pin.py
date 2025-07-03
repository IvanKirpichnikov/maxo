from maxo.types.base import MaxoType
from maxo.types.message.message import Message


class GetMessagePinResult(MaxoType):
    message: Message | None = None
