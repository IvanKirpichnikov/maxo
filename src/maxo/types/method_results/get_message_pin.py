from maxo.types.base import MaxoType
from maxo.types.types.message import Message


class GetMessagePinResult(MaxoType):
    message: Message | None = None
