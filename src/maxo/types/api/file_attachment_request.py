from typing import Self

from maxo.types.api.uploaded_info import UploadedInfo
from maxo.types.base import MaxoType


class FileAttachmentRequest(MaxoType):
    """
    Запрос на прикрепление файла.

    Args:
        payload: Данные запроса на прикрепление файла.

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
