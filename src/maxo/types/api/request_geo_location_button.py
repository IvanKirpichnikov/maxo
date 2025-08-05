from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class RequestGeoLocationKeyboardButton(MaxoType):
    """
    Инлайн кнопка запроса геолокации.

    Args:
        text: Видимый текст кнопки. От 1 до 128 символов.
        quick: Если true, отправляет местоположение без запроса подтверждения пользователя.

    """

    text: str
    quick: Omittable[bool] = Omitted()
