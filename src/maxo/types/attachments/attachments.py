from decimal import Decimal

from typing_extensions import Self

from maxo.enums.attachment_type import AttachmentType
from maxo.omit import Omittable, Omitted
from maxo.types.attachments.payloads import (
    ContactAttachmentPayload,
    FileAttachmentPayload,
    KeyboardPayloadAttachment,
    MediaAttachmentPayload,
    PhotoAttachmentPayload,
    ShareAttachmentPayload,
    StickerAttachmentPayload,
)
from maxo.types.base import MaxoType
from maxo.types.keyboard_buttons import KeyboardButtons
from maxo.types.user.user import User


class AudioAttachment(MaxoType):
    type = AttachmentType.AUDIO

    payload: MediaAttachmentPayload
    transcription: Omittable[str | None] = Omitted()

    @classmethod
    def factory(
        cls,
        url: str,
        token: Omittable[str] = Omitted(),
        transcription: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=MediaAttachmentPayload(
                url=url,
                token=token,
            ),
            transcription=transcription,
        )


class ContactAttachment(MaxoType):
    type = AttachmentType.CONTACT

    payload: ContactAttachmentPayload

    @classmethod
    def factory(
        cls,
        max_info: User | None = None,
        vcf_info: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=ContactAttachmentPayload(
                max_info=max_info,
                vcf_info=vcf_info,
            ),
        )


class FileAttachment(MaxoType):
    type = AttachmentType.FILE

    payload: FileAttachmentPayload
    filename: Omittable[str] = Omitted()
    size: Omittable[int] = Omitted()

    @classmethod
    def factory(
        cls,
        url: str,
        token: Omittable[str] = Omitted(),
        filename: Omittable[str] = Omitted(),
        size: Omittable[int] = Omitted(),
    ) -> Self:
        return cls(
            payload=FileAttachmentPayload(
                url=url,
                token=token,
            ),
            filename=filename,
            size=size,
        )


class ImageAttachment(MaxoType):
    type = AttachmentType.IMAGE

    payload: PhotoAttachmentPayload

    @classmethod
    def factory(
        cls,
        photo_id: int,
        token: str,
        url: str,
    ) -> Self:
        return cls(
            payload=PhotoAttachmentPayload(
                photo_id=photo_id,
                token=token,
                url=url,
            ),
        )


class KeyboardAttachment(MaxoType):
    type = AttachmentType.INLINE_KEYBOARD

    payload: KeyboardPayloadAttachment

    @classmethod
    def factory(cls, buttons: list[list[KeyboardButtons]]) -> Self:
        return cls(
            payload=KeyboardPayloadAttachment(
                buttons=buttons,
            ),
        )


class LocationAttachment(MaxoType):
    type = AttachmentType.LOCATION

    latitude: Omittable[Decimal] = Omitted()
    longitude: Omittable[Decimal] = Omitted()

    @classmethod
    def factory(
        cls,
        latitude: Omittable[Decimal] = Omitted(),
        longitude: Omittable[Decimal] = Omitted(),
    ) -> Self:
        return cls(
            latitude=latitude,
            longitude=longitude,
        )


class ShareAttachment(MaxoType):
    type = AttachmentType.SHARE

    payload: ShareAttachmentPayload = ShareAttachmentPayload()
    title: Omittable[str | None] = Omitted()
    description: Omittable[str | None] = Omitted()
    image_url: Omittable[str | None] = Omitted()

    @classmethod
    def factory(
        cls,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
        title: Omittable[str | None] = Omitted(),
        description: Omittable[str | None] = Omitted(),
        image_url: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=ShareAttachmentPayload(
                url=url,
                token=token,
            ),
            title=title,
            description=description,
            image_url=image_url,
        )


class StickerAttachment(MaxoType):
    type = AttachmentType.STICKER

    payload: StickerAttachmentPayload
    width: Omittable[int] = Omitted()
    height: Omittable[int] = Omitted()

    @classmethod
    def factory(
        cls,
        url: str,
        code: Omittable[str] = Omitted(),
        width: Omittable[int] = Omitted(),
        height: Omittable[int] = Omitted(),
    ) -> Self:
        return cls(
            payload=StickerAttachmentPayload(
                url=url,
                code=code,
            ),
            width=width,
            height=height,
        )


class VideoThumbnail(MaxoType):
    url: str


class VideoAttachment(MaxoType):
    type = AttachmentType.VIDEO

    payload: MediaAttachmentPayload
    thumbnail: VideoThumbnail | None = None
    width: Omittable[int | None] = Omitted()
    height: Omittable[int | None] = Omitted()
    duration: Omittable[int | None] = Omitted()

    @classmethod
    def factory(
        cls,
        url: str,
        token: Omittable[str] = Omitted(),
        thumbnail_url: str | None = None,
        width: Omittable[int | None] = Omitted(),
        height: Omittable[int | None] = Omitted(),
        duration: Omittable[int | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=MediaAttachmentPayload(
                url=url,
                token=token,
            ),
            thumbnail=VideoThumbnail(url=thumbnail_url) if thumbnail_url is not None else None,
            width=width,
            height=height,
            duration=duration,
        )


Attachments = (
    ImageAttachment
    | VideoAttachment
    | AudioAttachment
    | FileAttachment
    | StickerAttachment
    | ContactAttachment
    | KeyboardAttachment
    | ShareAttachment
    | LocationAttachment
)
