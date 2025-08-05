from typing import Self, Sequence

from maxo.types.api.inline_keyboard_attachment_request_payload import (
    InlineKeyboardAttachmentRequestPayload,
)
from maxo.types.api.keyboard_buttons import KeyboardButtons
from maxo.types.base import MaxoType


class InlineKeyboardAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление inline клавиатуры.

    Args:
        payload: Полезная нагрузка для запроса на прикрепление inline клавиатуры.

    """

    payload: InlineKeyboardAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        buttons: Sequence[Sequence[KeyboardButtons]],
    ) -> Self:
        return cls(
            payload=InlineKeyboardAttachmentRequestPayload(
                buttons=buttons,
            ),
        )
