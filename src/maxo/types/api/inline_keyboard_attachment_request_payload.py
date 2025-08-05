from typing import Sequence

from maxo.types.api.keyboard_buttons import KeyboardButtons
from maxo.types.base import MaxoType


class InlineKeyboardAttachmentRequestPayload(MaxoType):
    """
    Полезная нагрузка для запроса на прикрепление inline клавиатуры.

    Args:
        buttons: Двумерный массив кнопок. От 1 элемента

    """

    buttons: Sequence[Sequence[KeyboardButtons]]
