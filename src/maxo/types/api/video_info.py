from maxo.omit import Omittable, Omitted
from maxo.types.api.photo_attachment_payload import PhotoAttachmentPayload
from maxo.types.api.video_urls import VideoUrls
from maxo.types.base import MaxoType


class VideoInfo(MaxoType):
    """
    Информация о видео.

    Args:
        token: Токен видео-вложения
        urls:
            URL-ы для скачивания или воспроизведения видео.
            Может быть null, если видео недоступно.
        thumbnail: Миниатюра видео
        width: Ширина видео
        height: Высота видео
        duration: Длина видео в секундах

    """

    token: str
    urls: Omittable[VideoUrls | None] = Omitted()
    thumbnail: Omittable[PhotoAttachmentPayload] = Omitted()
    width: int
    height: int
    duration: int
