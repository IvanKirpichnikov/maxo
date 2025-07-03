from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.keyboard_buttons import KeyboardButtons
from maxo.kerno.types.types.user import User
from maxo.omit import Omittable, Omitted


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
