from maxo.types.base import MaxoType


class RequestContactKeyboardButton(MaxoType):
    """
    Инлайн кнопка запроса контакта.

    Args:
        text: Видимый текст кнопки. От 1 до 128 символов.

    """

    text: str
