from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.message import Message


class GetMessagePinResult(MaxoType):
    message: Message | None = None
