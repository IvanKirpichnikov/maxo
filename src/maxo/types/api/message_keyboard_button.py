from maxo.types.base import MaxoType


class MessageKeyboardButton(MaxoType):
    """
    Инлайн кнопка, текст которого будет отправлен в чат.

    Args:
        text: Текст кнопки, который будет отправлен в чат от лица пользователя. От 1 до 128 символов.

    """

    text: str
