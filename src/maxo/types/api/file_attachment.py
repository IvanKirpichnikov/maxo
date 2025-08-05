from typing import Self

from maxo.types.api.file_attachment_payload import FileAttachmentPayload
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class FileAttachment(MaxoType):
    """
    Файловое вложение.

    Args:
        payload: Содержимое файлового вложения.
        filename: Имя загруженного файла
        size: Размер файла в байтах

    """

    type = AttachmentType.FILE

    payload: FileAttachmentPayload
    filename: str
    size: int

    @classmethod
    def factory(
        cls,
        url: str,
        token: str,
        filename: str,
        size: int,
    ) -> Self:
        """
        Фабричный метод.

        Args:
            url: URL медиа-вложения. Для видео-вложения используйте метод `GetVideoAttachmentDetails`, чтобы получить прямые ссылки.
            token: Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении.
            filename: Имя загруженного файла
            size: Размер файла в байтах

        """
        return cls(
            payload=FileAttachmentPayload(
                url=url,
                token=token,
            ),
            filename=filename,
            size=size,
        )
