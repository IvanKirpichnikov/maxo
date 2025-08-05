from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class BotCommand(MaxoType):
    """
    Команда, поддерживаемая ботом.

    Args:
        name: Название команды. От 1 до 64 символов.
        description: Описание команды (по желанию). От 1 до 128 символов.

    """

    name: str
    description: Omittable[str | None] = Omitted()
