from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.keyboard_buttons import KeyboardButtons
from maxo.types.user.user import User


class ContactAttachmentPayload(MaxoType):
    vcf_info: Omittable[str | None] = Omitted()
    max_info: User | None = None


class FileAttachmentPayload(MaxoType):
    url: str
    token: Omittable[str] = Omitted()


class KeyboardPayloadAttachment(MaxoType):
    buttons: list[list[KeyboardButtons]]


class MediaAttachmentPayload(MaxoType):
    url: str
    token: Omittable[str] = Omitted()


class PhotoAttachmentPayload(MaxoType):
    photo_id: int
    token: str
    url: str


class ShareAttachmentPayload(MaxoType):
    url: Omittable[str | None] = Omitted()
    token: Omittable[str | None] = Omitted()


class StickerAttachmentPayload(MaxoType):
    url: str
    code: Omittable[str] = Omitted()
