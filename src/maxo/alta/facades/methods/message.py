import asyncio
from abc import ABC, abstractmethod
from collections.abc import Sequence

from maxo.alta.facades.methods.base import BaseMethodsFacade
from maxo.alta.facades.methods.upload_media import UploadMediaFacade
from maxo.alta.helpers.calculating import calculate_chat_id_and_user_id
from maxo.alta.upload_media import UploadMedia
from maxo.bot.method_results.messages.delete_message import DeleteMessageResult
from maxo.omit import Omittable, Omitted
from maxo.types.api.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from maxo.types.api.inline_keyboard_attachment_request_payload import (
    InlineKeyboardAttachmentRequestPayload,
)
from maxo.types.api.keyboard_buttons import KeyboardButtons
from maxo.types.api.message import Message
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.api.request_attachments import AttachmentsRequests, MediaAttachmentsRequests
from maxo.types.enums.message_link_type import MessageLinkType
from maxo.types.enums.text_fromat import TextFormat
from maxo.types.enums.upload_type import UploadType


class MessageMethodsFacade(BaseMethodsFacade, ABC):
    @property
    @abstractmethod
    def message(self) -> Message:
        raise NotImplementedError

    async def delete_message(self) -> DeleteMessageResult:
        message_id = self.message.unsafe_body.mid
        return await self.bot.delete_message(message_id=message_id)

    async def send_message(
        self,
        text: str | None = None,
        link: NewMessageLink | None = None,
        notify: Omittable[bool] = True,
        format: TextFormat | None = None,
        disable_link_preview: Omittable[bool] = Omitted(),
        attachments: Sequence[AttachmentsRequests] | None = None,
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        media: Sequence[UploadMedia] | None = None,
    ) -> Message:
        recipient = self.message.recipient
        chat_id, user_id = calculate_chat_id_and_user_id(
            chat_id=recipient.chat_id,
            user_id=recipient.user_id,
            chat_type=recipient.chat_type,
        )

        new_attachments = list(attachments) if attachments is not None else []

        if keyboard:
            new_attachments.append(InlineKeyboardAttachmentRequest.factory(keyboard))

        result = await self.bot.send_message(
            chat_id=chat_id or Omitted(),
            user_id=user_id or Omitted(),
            text=text,
            attachments=new_attachments,
            link=link,
            notify=notify,
            format=format,
            disable_link_preview=disable_link_preview,
        )
        return result.message

    async def answer_text(
        self,
        text: str,
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        notify: Omittable[bool] = True,
        format: TextFormat | None = None,
        disable_link_preview: Omittable[bool] = Omitted(),
    ) -> Message:
        return await self.send_message(
            text=text,
            notify=notify,
            format=format,
            keyboard=keyboard,
            disable_link_preview=disable_link_preview,
        )

    async def reply_text(
        self,
        text: str,
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        notify: Omittable[bool] = True,
        format: TextFormat | None = None,
        disable_link_preview: Omittable[bool] = Omitted(),
    ) -> Message:
        return await self.send_message(
            text=text,
            notify=notify,
            format=format,
            keyboard=keyboard,
            disable_link_preview=disable_link_preview,
            link=self._make_new_message_link(MessageLinkType.REPLY),
        )

    async def send_media(
        self,
        media: UploadMedia | Sequence[UploadMedia],
        text: str | None = None,
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        notify: Omittable[bool] = True,
        format: TextFormat | None = None,
        disable_link_preview: Omittable[bool] = Omitted(),
    ) -> Message:
        if isinstance(media, UploadMedia):
            media = (media,)

        return await self.send_message(
            text=text,
            media=media,
            notify=notify,
            format=format,
            keyboard=keyboard,
            disable_link_preview=disable_link_preview,
            link=self._make_new_message_link(MessageLinkType.REPLY),
        )

    def _make_new_message_link(self, type: MessageLinkType) -> NewMessageLink:
        return NewMessageLink(
            type=type,
            mid=self.message.unsafe_body.mid,
        )

    async def _build_attachments(
        self,
        base: Sequence[AttachmentsRequests],
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        media: Sequence[UploadMedia] | None = None,
    ) -> Sequence[AttachmentsRequests]:
        attachments = list(base)

        if keyboard is not None:
            attachments.append(
                InlineKeyboardAttachmentRequest(
                    payload=InlineKeyboardAttachmentRequestPayload(buttons=keyboard),
                )
            )

        if media:
            attachments.extend(await self._build_media_attachments(media))

        return attachments

    async def _build_media_attachments(
        self,
        media: Sequence[UploadMedia],
    ) -> Sequence[MediaAttachmentsRequests]:
        attachments: list[MediaAttachmentsRequests] = []

        await asyncio.gather(*[asyncio.create_task(self._upload_media(upload_media)) for upload_media in media])

        # for type, token in result:
        #     match type:
        #         case UploadType.IMAGE:
        #             attachments.append(ImageAttachmentRequest())

        return attachments

    async def _upload_media(self, media: UploadMedia) -> tuple[UploadType, str]:
        token = await UploadMediaFacade(self.bot, media).upload()
        return media.type, token.last_token
