from typing import Self

from maxo.types.api.uploaded_info import UploadedInfo
from maxo.types.base import MaxoType


class AudioAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление аудио.

    Args:
        payload: Данные запроса на прикрепление аудио.

    """

    payload: UploadedInfo

    @classmethod
    def factory(cls, token: str) -> Self:
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
