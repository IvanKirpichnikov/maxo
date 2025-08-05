from abc import abstractmethod
from collections.abc import Sequence

from maxo.alta.facades.methods.base import BaseMethodsFacade
from maxo.alta.helpers.calculating import calculate_chat_id_and_user_id
from maxo.alta.upload_media import UploadMedia
from maxo.omit import Omittable, Omitted
from maxo.types.api.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from maxo.types.api.keyboard_buttons import KeyboardButtons
from maxo.types.api.message import Message
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.api.request_attachments import MediaAttachmentsRequests
from maxo.types.enums.text_fromat import TextFormat


class SendMessageFacade(BaseMethodsFacade):
    @property
    @abstractmethod
    def message(self) -> Message:
        raise NotImplementedError

    async def _send_message(
        self,
        text: str | None = None,
        link: NewMessageLink | None = None,
        notify: Omittable[bool] = True,
        format: TextFormat | None = None,
        disable_link_preview: Omittable[bool] = Omitted(),
        # Attachments
        keyboard: Sequence[Sequence[KeyboardButtons]] | None = None,
        media: Sequence[UploadMedia | MediaAttachmentsRequests] | None = None,
    ) -> Message:
        recipient = self.message.recipient
        chat_id, user_id = calculate_chat_id_and_user_id(
            chat_type=recipient.chat_type,
            chat_id=recipient.chat_id,
            user_id=recipient.user_id,
        )

        attachments = []

        if keyboard:
            attachments.append(InlineKeyboardAttachmentRequest.factory(keyboard))

        result = await self.bot.send_message(
            chat_id=chat_id or Omitted(),
            user_id=user_id or Omitted(),
            text=text,
            attachments=attachments,
            link=link,
            notify=notify,
            format=format,
            disable_link_preview=disable_link_preview,
        )
        return result.message
