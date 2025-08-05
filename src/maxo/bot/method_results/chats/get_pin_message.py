from maxo.omit import Omittable, Omitted
from maxo.types.api.message import Message
from maxo.types.base import MaxoType


class GetPinMessageResult(MaxoType):
    """
    Результат получения закрепленного сообщения.

    Args:
        message:
        Закрепленное сообщение.
        Может быть null, если в чате нет закрепленного сообщения.

    """

    message: Omittable[Message | None] = Omitted()
