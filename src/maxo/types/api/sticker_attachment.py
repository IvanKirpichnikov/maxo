from typing import Self

from maxo.types.api.sticker_attachment_payload import StickerAttachmentPayload
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class StickerAttachment(MaxoType):
    """
    Вложение стикера.

    Args:
        payload: Данные вложения стикера.
        width: Ширина стикера.
        height: Высота стикера.

    """

    type = AttachmentType.STICKER

    payload: StickerAttachmentPayload
    width: int
    height: int

    @classmethod
    def factory(
        cls,
        url: str,
        code: str,
        width: int,
        height: int,
    ) -> Self:
        """
        Фабричный метод.

        Args:
            url: URL медиа-вложения. Для видео-вложения используйте метод `GetVideoAttachmentDetails`, чтобы получить прямые ссылки.
            code: ID стикера.
            width: Ширина стикера.
            height: Высота стикера.

        """
        return cls(
            payload=StickerAttachmentPayload(
                url=url,
                code=code,
            ),
            width=width,
            height=height,
        )
