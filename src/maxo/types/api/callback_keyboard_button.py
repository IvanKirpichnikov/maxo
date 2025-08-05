from maxo.omit import Omittable
from maxo.types.base import MaxoType
from maxo.types.enums.intent import IntentType


class CallbackKeyboardButton(MaxoType):
    """
    Инлайн кнопка с токеном.

    Args:
        text: Видимый текст кнопки. От 1 до 128 символов.
        payload: Токен кнопки. До 1024 символов.
        intent: Намерение кнопки. Влияет на отображение клиентом.

    """

    text: str
    payload: str
    intent: Omittable[IntentType] = IntentType.DEFAULT
