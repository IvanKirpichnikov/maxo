from collections.abc import Sequence
from decimal import Decimal

from typing_extensions import Self

from maxo.omit import Omittable, Omitted
from maxo.types.attachments.payloads import ShareAttachmentPayload
from maxo.types.base import MaxoType
from maxo.types.keyboard_buttons import KeyboardButtons
from maxo.types.request_attachments.payloads import (
    ContactAttachmentRequestPayload,
    InlineKeyboardAttachmentRequestPayload,
    PhotoAttachmentRequestPayload,
    StickerAttachmentRequestPayload,
    UploadedInfo,
)


class ImageAttachmentRequest(MaxoType):
    payload: PhotoAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
        photos: Omittable[list[str] | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=PhotoAttachmentRequestPayload(
                url=url,
                token=token,
                photos=photos,
            ),
        )


class VideoAttachmentRequest(MaxoType):
    payload: UploadedInfo

    @classmethod
    def factory(
        cls,
        token: Omittable[str] = Omitted(),
    ) -> Self:
        return cls(
            payload=UploadedInfo(
                token=token,
            ),
        )


class AudioAttachmentRequest(MaxoType):
    payload: UploadedInfo

    @classmethod
    def factory(
        cls,
        token: Omittable[str] = Omitted(),
    ) -> Self:
        return cls(
            payload=UploadedInfo(
                token=token,
            ),
        )


class FileAttachmentRequest(MaxoType):
    payload: UploadedInfo

    @classmethod
    def factory(
        cls,
        token: Omittable[str] = Omitted(),
    ) -> Self:
        return cls(
            payload=UploadedInfo(
                token=token,
            ),
        )


class StickerAttachmentRequest(MaxoType):
    payload: StickerAttachmentRequestPayload

    @classmethod
    def factory(cls, code: str) -> Self:
        return cls(
            payload=StickerAttachmentRequestPayload(
                code=code,
            ),
        )


class ContactAttachmentRequest(MaxoType):
    payload: ContactAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        name: str | None = None,
        contact_id: Omittable[int | None] = Omitted(),
        vcf_info: Omittable[str | None] = Omitted(),
        vcf_phone: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=ContactAttachmentRequestPayload(
                name=name,
                contact_id=contact_id,
                vcf_info=vcf_info,
                vcf_phone=vcf_phone,
            ),
        )


class InlineKeyboardAttachmentRequest(MaxoType):
    payload: InlineKeyboardAttachmentRequestPayload

    @classmethod
    def factory(
        cls,
        buttons: Sequence[Sequence[KeyboardButtons]],
    ) -> Self:
        return cls(
            payload=InlineKeyboardAttachmentRequestPayload(
                buttons=buttons,
            ),
        )


class LocationAttachmentRequest(MaxoType):
    latitude: Omittable[Decimal] = Omitted()
    longitude: Omittable[Decimal] = Omitted()


class ShareAttachmentRequest(MaxoType):
    payload: ShareAttachmentPayload

    @classmethod
    def factory(
        cls,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=ShareAttachmentPayload(
                url=url,
                token=token,
            ),
        )


MediaAttachmentsRequests = (
    ImageAttachmentRequest | VideoAttachmentRequest | AudioAttachmentRequest | FileAttachmentRequest
)

AttachmentsRequests = (
    MediaAttachmentsRequests
    | StickerAttachmentRequest
    | ContactAttachmentRequest
    | InlineKeyboardAttachmentRequest
    | LocationAttachmentRequest
    | ShareAttachmentRequest
)
