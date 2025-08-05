from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.share_attachment_payload import ShareAttachmentPayload
from maxo.types.base import MaxoType


class ShareAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление вложения обмена.

    Args:
        payload: Полезная нагрузка вложения обмена.

    """

    payload: ShareAttachmentPayload

    @classmethod
    def factory(
        cls,
        *,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
    ) -> Self:
        """
        Фабричный метод.

        Args:
            url: URL, прикрепленный к сообщению в качестве предпросмотра медиа. От 1 символа.
            token: Токен вложения.

        """
        return cls(
            payload=ShareAttachmentPayload(
                url=url,
                token=token,
            ),
        )
