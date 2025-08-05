from maxo.types.base import MaxoType


class LinkKeyboardButton(MaxoType):
    """
    Инлайн кнопка с ссылкой.

    Args:
        text: Видимый текст кнопки. От 1 до 128 символов.
        url: Ссылка. до 2048 символов

    """

    text: str
    url: str
