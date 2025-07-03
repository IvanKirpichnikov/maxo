from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.types.payload_attachments import PhotoAttachmentPayload


class VideoUrls(MaxoType):
    mp4_1080: Omittable[str | None] = Omitted()
    mp4_720: Omittable[str | None] = Omitted()
    mp4_480: Omittable[str | None] = Omitted()
    mp4_360: Omittable[str | None] = Omitted()
    mp4_240: Omittable[str | None] = Omitted()
    mp4_144: Omittable[str | None] = Omitted()
    hls: Omittable[str | None] = Omitted()


class VideoInfo(MaxoType):
    token: str
    width: int
    height: int
    duration: int
    urls: VideoUrls | None = None
    thumbnail: PhotoAttachmentPayload | None = None
