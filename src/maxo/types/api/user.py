from datetime import datetime

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class User(MaxoType):
    """
    Информация о пользователе.

    Args:
        user_id: ID пользователя.
        first_name: Отображаемое имя пользователя.
        last_name: Отображаемая фамилия пользователя.
        username:
            Уникальное публичное имя пользователя.
            Может быть null, если пользователь недоступен или имя не задано.
        is_bot: True, если пользователь является ботом.
        last_activity_time:
            Время последней активности пользователя в MAX (Unix-время в миллисекундах).
            Может быть неактуальным, если пользователь отключил статус "онлайн" в настройках.
        description:
            Описание пользователя.
            Может быть null, если пользователь его не заполнил.
            До 16000 символов.

    """

    user_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    is_bot: bool
    last_activity_time: datetime
    description: Omittable[str | None] = Omitted()
