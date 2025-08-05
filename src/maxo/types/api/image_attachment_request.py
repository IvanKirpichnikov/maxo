from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.photo_attachment_request_payload import PhotoAttachmentRequestPayload
from maxo.types.base import MaxoType


class ImageAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление изображения.

    Args:
        payload: Данные запроса на прикрепление изображения

    """

    payload: PhotoAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        *,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
        photos: Omittable[list[str] | None] = Omitted(),
    ) -> Self:
        """
        Фабричный метод.

        Все поля являются взаимоисключающими.

        Args:
            url: Любой внешний URL изображения, которое вы хотите прикрепить. От 1 символа.
            token: Токен существующего вложения.
            photos: Токены, полученные после загрузки изображений

        """
        return cls(
            payload=PhotoAttachmentRequestPayload(
                url=url,
                token=token,
                photos=photos,
            ),
        )
