from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class OpenAppKeyboardButton(MaxoType):
    """
    Инлайн кнопка для открытия приложения.

    Args:
        text: Видимый текст кнопки. От 1 до 128 символов.
        web_app: Публичное имя (username) бота или ссылка на него, чьё мини-приложение надо запустить.
        contact_id: Идентификатор бота, чьё мини-приложение надо запустить.

    """

    text: str
    web_app: Omittable[str] = Omitted()
    contact_id: Omittable[int] = Omitted()
