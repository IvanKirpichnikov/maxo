from retejo.http.markers import UrlVar

from maxo.bot.methods.base import MaxoMethod
from maxo.types.api.video_info import VideoInfo


class GetVideoInfo(MaxoMethod[VideoInfo]):
    """
    Получить информацио о видео.

    Возвращает подробную информацию о приклеплённом видео.
    URL-адреса воспроизведения и дополнительные метаданные.

    Источник: https://dev.max.ru/docs-api/methods/GET/videos/-videoToken-

    Args:
        video_token: Токен видео-вложения.

    """

    __url__ = "videos/{video_token}"
    __http_method__ = "get"

    video_token: UrlVar[str]
