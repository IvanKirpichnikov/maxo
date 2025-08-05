from maxo.omit import Omittable, Omitted
from maxo.types.api.message_body import MessageBody
from maxo.types.api.user import User
from maxo.types.base import MaxoType
from maxo.types.enums.message_link_type import MessageLinkType


class LinkedMessage(MaxoType):
    """
    Пересланное или ответное сообщение.

    Args:
        type: Тип связанного сообщения.
        sender: Пользователь, отправивший сообщение.
        chat_id: Чат, в котором сообщение было изначально опубликовано. Только для пересланных сообщений
        message: Схема, представляющая тело сообщения

    """

    type: MessageLinkType
    sender: Omittable[User] = Omitted()
    chat_id: Omittable[int] = Omitted()
    message: MessageBody
