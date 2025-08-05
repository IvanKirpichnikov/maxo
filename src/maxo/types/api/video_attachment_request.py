from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.uploaded_info import UploadedInfo
from maxo.types.base import MaxoType


class VideoAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление изображения.

    Args:
        payload: Данные запроса на прикрепление изображения

    """

    payload: UploadedInfo

    @classmethod
    def factory(cls, token: Omittable[str] = Omitted()) -> Self:
        """
        Фабричный метод.

        Args:
            token: Токен — уникальный ID загруженного медиафайла.

        """
        return cls(
            payload=UploadedInfo(
                token=token,
            ),
        )
