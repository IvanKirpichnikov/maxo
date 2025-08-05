from datetime import datetime
from typing import Any

from maxo.omit import Omittable, Omitted
from maxo.types.api.image import Image
from maxo.types.api.message import Message
from maxo.types.api.user_with_photo import UserWithPhoto
from maxo.types.base import MaxoType
from maxo.types.enums.chat_status import ChatStatusType
from maxo.types.enums.chat_type import ChatType


class Chat(MaxoType):
    """
    Чат.

    Args:
        chat_id: ID чата.
        type: Тип чата.
        status: Статус чата.
        title: Отображаемое название чата. Может быть null для диалогов.
        icon: Иконка чата.
        last_event_time: Время последнего события в чате.
        participants_count: Количество участников чата. Для диалогов всегда 2.
        owner_id: ID владельца чата.
        participants:
            Участники чата с временем последней активности.
            Может быть null, если запрашивается список чатов.
        is_public: Доступен ли чат публично (для диалогов всегда false).
        link: Ссылка на чат.
        description: Описание чата.
        dialog_with_user: Данные о пользователе в диалоге (только для чатов типа "dialog").
        messages_count: Количество сообщений в чате (доступно только для групповых чатов, недоступно для диалогов).
        chat_message_id: ID сообщения, содержащего кнопку, через которую был инициирован чат.
        pinned_message: Закреплённое сообщение в чате (возвращается только при запросе конкретного чата).

    """

    chat_id: int
    type: ChatType
    status: ChatStatusType
    title: str | None = None
    icon: Image | None = None
    last_event_time: datetime
    participants_count: int
    owner_id: Omittable[int | None] = Omitted()
    participants: Omittable[Any | None] = Omitted()
    is_public: bool
    link: Omittable[str | None] = Omitted()
    description: str | None = None
    dialog_with_user: Omittable[UserWithPhoto | None] = Omitted()
    messages_count: Omittable[int | None] = Omitted()
    chat_message_id: Omittable[str | None] = Omitted()
    pinned_message: Omittable[Message | None] = Omitted()
