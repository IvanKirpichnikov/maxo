from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.keyboard_buttons import KeyboardButtons


class PhotoAttachmentRequestPayload(MaxoType):
    url: Omittable[str | None] = Omitted()
    token: Omittable[str | None] = Omitted()
    photos: Omittable[list[str] | None] = Omitted()


class UploadedInfo(MaxoType):
    token: Omittable[str] = Omitted()


class StickerAttachmentRequestPayload(MaxoType):
    code: str


class ContactAttachmentRequestPayload(MaxoType):
    name: str | None = None
    contact_id: Omittable[int | None] = Omitted()
    vcf_info: Omittable[str | None] = Omitted()
    vcf_phone: Omittable[str | None] = Omitted()


class InlineKeyboardAttachmentRequestPayload(MaxoType):
    buttons: Sequence[Sequence[KeyboardButtons]]
