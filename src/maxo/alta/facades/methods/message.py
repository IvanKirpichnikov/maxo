import asyncio
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import cast

from typing_extensions import assert_never

from maxo.alta.facades.methods.base import BaseMethodsFacade
from maxo.alta.facades.methods.upload_media import UploadMediaFacade
from maxo.kerno.types.enums.chat_type import ChatType
from maxo.kerno.types.enums.message_link_type import MessageLinkType
from maxo.kerno.types.enums.text_fromat import TextFormat
from maxo.kerno.types.enums.upload_type import UploadType
from maxo.kerno.types.method_results.method import MethodResult
from maxo.kerno.types.types.keyboard_buttons import Keyboard
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.types.new_message_link import NewMessageLink
from maxo.kerno.types.types.payload_request_attachments import (
    InlineKeyboardAttachmentRequestPayload,
)
from maxo.kerno.types.types.request_attachments import (
    AttachmentsRequests,
    InlineKeyboardAttachmentRequest,
    MediaAttachmentsRequests,
)
from maxo.kerno.types.upload_media import UploadMedia
from maxo.omit import Omittable, Omitted


class MessageMethodsFacade(BaseMethodsFacade, ABC):
    @property
    @abstractmethod
    def message(self) -> Message:
        raise NotImplementedError

    async def delete_message(self) -> MethodResult:
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
        keyboard: Keyboard | None = None,
        media: Sequence[UploadMedia] | None = None,
    ) -> Message:
        chat_id, user_id = self._load_chat_id_and_user_id()

        new_attachments = list(attachments) if attachments is not None else []

        if keyboard:
            new_attachments.append(InlineKeyboardAttachmentRequest.factory(keyboard))

        result = await self.bot.send_message(
            chat_id=chat_id,
            user_id=user_id,
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
        keyboard: Keyboard | None = None,
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
        keyboard: Keyboard | None = None,
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
        keyboard: Keyboard | None = None,
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

    def _load_chat_id_and_user_id(
        self,
    ) -> tuple[Omittable[int], Omittable[int]]:
        chat_id: Omittable[int]
        user_id: Omittable[int]

        recipient = self.message.recipient
        if recipient.chat_type is ChatType.CHAT:
            user_id = Omitted()
            chat_id = cast("int", recipient.chat_id)
        elif recipient.chat_type is ChatType.DIALOG:
            chat_id = cast("int", recipient.chat_id)
            user_id = cast("int", recipient.user_id)
        else:
            assert_never(recipient.chat_type)

        return chat_id, user_id

    async def _build_attachments(
        self,
        base: Sequence[AttachmentsRequests],
        keyboard: Keyboard | None = None,
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
