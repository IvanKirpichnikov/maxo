from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class VideoUrls(MaxoType):
    """
    URL-ы видео.

    Args:
        mp4_1080: URL видео в разрешении 1080p, если доступно
        mp4_720: URL видео в разрешении 720p, если доступно
        mp4_480: URL видео в разрешении 480p, если доступно
        mp4_360: URL видео в разрешении 360p, если доступно
        mp4_240: URL видео в разрешении 240p, если доступно
        mp4_144: URL видео в разрешении 144p, если доступно
        hls: URL трансляции, если доступна

    """

    mp4_1080: Omittable[str | None] = Omitted()
    mp4_720: Omittable[str | None] = Omitted()
    mp4_480: Omittable[str | None] = Omitted()
    mp4_360: Omittable[str | None] = Omitted()
    mp4_240: Omittable[str | None] = Omitted()
    mp4_144: Omittable[str | None] = Omitted()
    hls: Omittable[str | None] = Omitted()
