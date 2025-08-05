from typing import Sequence

from maxo.types.api.keyboard_buttons import KeyboardButtons
from maxo.types.base import MaxoType


class Keyboard(MaxoType):
    """
    Клавиатура.

    Args:
        buttons: Двумерный массив кнопок.

    """

    buttons: Sequence[Sequence[KeyboardButtons]]
