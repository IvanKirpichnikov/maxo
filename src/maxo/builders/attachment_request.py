from collections.abc import Sequence
from decimal import Decimal

from typing_extensions import Self

from maxo.omit import Omittable, Omitted
from maxo.types.keyboard_buttons import KeyboardButtons
from maxo.types.request_attachments.attachments import (
    AttachmentsRequests,
    AudioAttachmentRequest,
    ContactAttachmentRequest,
    FileAttachmentRequest,
    ImageAttachmentRequest,
    InlineKeyboardAttachmentRequest,
    LocationAttachmentRequest,
    ShareAttachmentRequest,
    StickerAttachmentRequest,
    VideoAttachmentRequest,
)


class AttachmentRequestBuilder:
    def __init__(self) -> None:
        self._items: list[AttachmentsRequests] = []

    def build(self) -> list[AttachmentsRequests]:
        return self._items

    def add_image(
        self,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
        photos: Omittable[list[str] | None] = Omitted(),
    ) -> Self:
        self._items.append(
            ImageAttachmentRequest.factory(
                url=url,
                token=token,
                photos=photos,
            )
        )
        return self

    def add_video(self, token: str) -> Self:
        self._items.append(VideoAttachmentRequest.factory(token=token))
        return self

    def add_audio(self, token: str) -> Self:
        self._items.append(AudioAttachmentRequest.factory(token=token))
        return self

    def add_file(self, token: str) -> Self:
        self._items.append(FileAttachmentRequest.factory(token=token))
        return self

    def add_sticker(self, code: str) -> Self:
        self._items.append(StickerAttachmentRequest.factory(code=code))
        return self

    def add_contact(
        self,
        name: str | None = None,
        contact_id: Omittable[int | None] = Omitted(),
        vcf_info: Omittable[str | None] = Omitted(),
        vcf_phone: Omittable[str | None] = Omitted(),
    ) -> Self:
        self._items.append(
            ContactAttachmentRequest.factory(
                name=name,
                contact_id=contact_id,
                vcf_info=vcf_info,
                vcf_phone=vcf_phone,
            )
        )
        return self

    def add_inline_keyboard(self, buttons: Sequence[Sequence[KeyboardButtons]]) -> Self:
        self._items.append(
            InlineKeyboardAttachmentRequest.factory(
                buttons=buttons,
            )
        )
        return self

    def add_location(self, latitude: Decimal, longitude: Decimal) -> Self:
        self._items.append(
            LocationAttachmentRequest(
                latitude=latitude,
                longitude=longitude,
            )
        )
        return self

    def add_share(
        self,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
    ) -> Self:
        self._items.append(
            ShareAttachmentRequest.factory(
                url=url,
                token=token,
            )
        )
        return self
