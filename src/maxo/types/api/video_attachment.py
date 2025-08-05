from typing import Self

from maxo.omit import Omittable, Omitted, is_not_omitted
from maxo.types.api.media_attachment_payload import MediaAttachmentPayload
from maxo.types.api.video_thumbnail import VideoThumbnail
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class VideoAttachment(MaxoType):
    """
    Видео вложение.

    Args:
        payload: Содержимое мультимедийного вложения.
        thumbnail: Миниатюра видео
        width: Ширина видео
        height: Высота видео
        duration: Длина видео в секундах

    """

    type = AttachmentType.VIDEO

    payload: MediaAttachmentPayload
    thumbnail: Omittable[VideoThumbnail | None] = Omitted()
    width: Omittable[int | None] = Omitted()
    height: Omittable[int | None] = Omitted()
    duration: Omittable[int | None] = Omitted()

    @classmethod
    def factory(
        cls,
        url: str,
        token: str,
        thumbnail_url: Omittable[str] = Omitted(),
        width: Omittable[int | None] = Omitted(),
        height: Omittable[int | None] = Omitted(),
        duration: Omittable[int | None] = Omitted(),
    ) -> Self:
        """
        Фабричный метод.

        Args:
            url: URL медиа-вложения. Для видео-вложения используйте метод GetVideoAttachmentDetails, чтобы получить прямые ссылки.
            token: Используйте token, если вы пытаетесь повторно использовать одно и то же вложение в другом сообщении..
            thumbnail_url: URL изображения
            width: Ширина видео
            height: Высота видео
            duration: Длина видео в секундах

        """
        thumbnail: Omittable[VideoThumbnail]

        if is_not_omitted(thumbnail_url):
            thumbnail = VideoThumbnail(url=thumbnail_url)
        else:
            thumbnail = Omitted()

        return cls(
            payload=MediaAttachmentPayload(
                url=url,
                token=token,
            ),
            thumbnail=thumbnail,
            width=width,
            height=height,
            duration=duration,
        )
