from typing import Self

from maxo.types.api.photo_attachment_payload import PhotoAttachmentPayload
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class ImageAttachment(MaxoType):
    """
    Вложение изображения.

    Args:
        payload: Содержимое вложения изображения.

    """

    type = AttachmentType.IMAGE

    payload: PhotoAttachmentPayload

    @classmethod
    def factory(
        cls,
        photo_id: int,
        token: str,
        url: str,
    ) -> Self:
        """
        Фабричный метод.

        Args:
            photo_id: Уникальный ID этого изображения
            token: Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении.
            url: URL изображения

        """
        return cls(
            payload=PhotoAttachmentPayload(
                photo_id=photo_id,
                token=token,
                url=url,
            ),
        )
