from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.video_info import VideoInfo


class GetVideoInfo(Method[VideoInfo]):
    __url__ = "videos/{video_token}"
    __method__ = "get"

    video_token: UrlVar[str]
