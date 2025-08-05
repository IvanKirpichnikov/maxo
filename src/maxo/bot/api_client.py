from datetime import datetime
from typing import Any

from adaptix import P, Retort, dumper, loader
from aiohttp import ClientResponse
from retejo.http.clients.aiohttp import AiohttpClient
from retejo.http.entities import HttpResponse
from retejo.http.markers import QueryParamMarker
from retejo.utils.for_marker import for_marker

from maxo._internal._adaptix.concat_provider import concat_provider
from maxo._internal._adaptix.has_tag_provider import has_tag_provider
from maxo.bot.warming_up import WarmingUpType, warming_up_retort
from maxo.errors.api import (
    MaxBotBadRequestError,
    MaxBotMethodNotAllowedError,
    MaxBotNotFoundError,
    MaxBotServiceUnavailableError,
    MaxBotTooManyRequestsError,
    MaxBotUnauthorizedError,
    MaxVotForbiddenError,
    RetvalReturnedServerException,
)
from maxo.routing.updates.bot_added import BotAdded
from maxo.routing.updates.bot_removed import BotRemoved
from maxo.routing.updates.bot_started import BotStarted
from maxo.routing.updates.chat_title_changed import ChatTitileChanged
from maxo.routing.updates.message_callback import MessageCallback
from maxo.routing.updates.message_chat_created import MessageChatCreated
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.updates.message_edited import MessageEdited
from maxo.routing.updates.message_removed import MessageRemoved
from maxo.routing.updates.user_added import UserAdded
from maxo.routing.updates.user_removed import UserRemoved
from maxo.types.api.audio_attachment import AudioAttachment
from maxo.types.api.audio_attachment_request import AudioAttachmentRequest
from maxo.types.api.callback_keyboard_button import CallbackKeyboardButton
from maxo.types.api.chat_keyboard_button import ChatKeyboardButton
from maxo.types.api.contact_attachment import ContactAttachment
from maxo.types.api.contact_attachment_request import ContactAttachmentRequest
from maxo.types.api.file_attachment import FileAttachment
from maxo.types.api.file_attachment_request import FileAttachmentRequest
from maxo.types.api.image_attachment import ImageAttachment
from maxo.types.api.image_attachment_request import ImageAttachmentRequest
from maxo.types.api.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from maxo.types.api.keyboard import Keyboard
from maxo.types.api.link_keyboard_button import LinkKeyboardButton
from maxo.types.api.location_attachment import LocationAttachment
from maxo.types.api.location_attachment_request import LocationAttachmentRequest
from maxo.types.api.markup_elements import (
    EmphasizedMarkupElement,
    HeadingMarkupElement,
    HighlightedMarkupElement,
    LinkMarkupElement,
    MonospacedMarkupElements,
    StrikethroughMarkupElement,
    StrongMarkupElement,
    UnderlineMarkupElement,
    UserMentionMarkupElement,
)
from maxo.types.api.message_keyboard_button import MessageKeyboardButton
from maxo.types.api.open_app_keyboard_button import OpenAppKeyboardButton
from maxo.types.api.request_contact_keyboard_button import RequestContactKeyboardButton
from maxo.types.api.request_geo_location_button import RequestGeoLocationKeyboardButton
from maxo.types.api.share_attachment import ShareAttachment
from maxo.types.api.share_attachment_request import ShareAttachmentRequest
from maxo.types.api.sticker_attachment import StickerAttachment
from maxo.types.api.sticker_attachment_request import StickerAttachmentRequest
from maxo.types.api.video_attachment import VideoAttachment
from maxo.types.api.video_attachment_request import VideoAttachmentRequest
from maxo.types.enums.attachment_request_type import AttachmentRequestType
from maxo.types.enums.attachment_type import AttachmentType
from maxo.types.enums.keyboard_button_type import KeyboardButtonType
from maxo.types.enums.markup_element_type import MarkupElementType

_has_tag_providers = concat_provider(
    # ---> UpdateType <---
    has_tag_provider(BotAdded, "update_type", "bot_added"),
    has_tag_provider(UserAdded, "update_type", "user_added"),
    has_tag_provider(MessageRemoved, "update_type", "message_removed"),
    has_tag_provider(MessageEdited, "update_type", "message_edited"),
    has_tag_provider(MessageCallback, "update_type", "message_callback"),
    has_tag_provider(MessageChatCreated, "update_type", "message_chat_created"),
    has_tag_provider(MessageCreated, "update_type", "message_created"),
    has_tag_provider(BotStarted, "update_type", "bot_started"),
    has_tag_provider(BotRemoved, "update_type", "bot_removed"),
    has_tag_provider(ChatTitileChanged, "update_type", "chat_title_changed"),
    has_tag_provider(UserRemoved, "update_type", "user_removed"),
    # ---> AttachmentType <---
    has_tag_provider(AudioAttachment, "type", AttachmentType.AUDIO),
    has_tag_provider(ContactAttachment, "type", AttachmentType.CONTACT),
    has_tag_provider(FileAttachment, "type", AttachmentType.FILE),
    has_tag_provider(ImageAttachment, "type", AttachmentType.IMAGE),
    has_tag_provider(Keyboard, "type", AttachmentType.INLINE_KEYBOARD),
    has_tag_provider(LocationAttachment, "type", AttachmentType.LOCATION),
    has_tag_provider(ShareAttachment, "type", AttachmentType.SHARE),
    has_tag_provider(StickerAttachment, "type", AttachmentType.STICKER),
    has_tag_provider(VideoAttachment, "type", AttachmentType.VIDEO),
    # ---> MarkupElementType <---
    has_tag_provider(EmphasizedMarkupElement, "type", MarkupElementType.EMPHASIZED),
    has_tag_provider(HeadingMarkupElement, "type", MarkupElementType.HEADING),
    has_tag_provider(HighlightedMarkupElement, "type", MarkupElementType.HIGHLIGHTED),
    has_tag_provider(LinkMarkupElement, "type", MarkupElementType.LINK),
    has_tag_provider(MonospacedMarkupElements, "type", MarkupElementType.MONOSPACED),
    has_tag_provider(StrikethroughMarkupElement, "type", MarkupElementType.STRIKETHROUGH),
    has_tag_provider(StrongMarkupElement, "type", MarkupElementType.STRONG),
    has_tag_provider(UnderlineMarkupElement, "type", MarkupElementType.UNDERLINE),
    has_tag_provider(UserMentionMarkupElement, "type", MarkupElementType.USER_MENTION),
    # ---> AttachmentRequestType <---
    has_tag_provider(ImageAttachmentRequest, "type", AttachmentRequestType.IMAGE),
    has_tag_provider(VideoAttachmentRequest, "type", AttachmentRequestType.VIDEO),
    has_tag_provider(AudioAttachmentRequest, "type", AttachmentRequestType.AUDIO),
    has_tag_provider(FileAttachmentRequest, "type", AttachmentRequestType.FILE),
    has_tag_provider(StickerAttachmentRequest, "type", AttachmentRequestType.STICKER),
    has_tag_provider(ContactAttachmentRequest, "type", AttachmentRequestType.CONTACT),
    has_tag_provider(
        InlineKeyboardAttachmentRequest,
        "type",
        AttachmentRequestType.INLINE_KEYBOARD,
    ),
    has_tag_provider(LocationAttachmentRequest, "type", AttachmentRequestType.LOCATION),
    has_tag_provider(ShareAttachmentRequest, "type", AttachmentRequestType.SHARE),
    # ---> KeyboardButtonType <---
    has_tag_provider(CallbackKeyboardButton, "type", KeyboardButtonType.CALLBACK),
    has_tag_provider(ChatKeyboardButton, "type", KeyboardButtonType.CHAT),
    has_tag_provider(LinkKeyboardButton, "type", KeyboardButtonType.LINK),
    has_tag_provider(
        RequestContactKeyboardButton,
        "type",
        KeyboardButtonType.REQUEST_CONTACT,
    ),
    has_tag_provider(
        RequestGeoLocationKeyboardButton,
        "type",
        KeyboardButtonType.REQUEST_GEO_LOCATION,
    ),
    has_tag_provider(
        OpenAppKeyboardButton,
        "type",
        KeyboardButtonType.REQUEST_GEO_LOCATION,
    ),
    has_tag_provider(
        MessageKeyboardButton,
        "type",
        KeyboardButtonType.MESSAGE,
    ),
)


class MaxApiClient(AiohttpClient):
    def __init__(
        self,
        token: str,
        warming_up: bool,
    ) -> None:
        self._warming_up = warming_up
        super().__init__(
            base_url="https://botapi.max.ru/",
            headers={"Authorization": token},
        )

    def init_method_dumper(self) -> Retort:
        retort = super().init_method_dumper().extend(
            recipe=[
                _has_tag_providers,
                dumper(
                    for_marker(P[None], QueryParamMarker),
                    lambda x: "null",
                ),
            ]
        )
        return warming_up_retort(
            retort,
            warming_up=WarmingUpType.METHOD if self._warming_up else None
        )

    def init_response_loader(self) -> Retort:
        retort = super().init_response_loader().extend(
            recipe=(
                _has_tag_providers,
                loader(P[datetime], lambda x: datetime.fromtimestamp(x / 1000)),
            ),
        )
        return warming_up_retort(
            retort,
            warming_up=WarmingUpType.TYPES if self._warming_up else None
        )

    async def retrieve_response_data(
        self,
        raw_response: ClientResponse,
    ) -> Any:
        text = await raw_response.text()
        if "retval" in text:
            raise RetvalReturnedServerException

        return await super().retrieve_response_data(raw_response)

    async def handle_error_response(
        self,
        response: HttpResponse[ClientResponse],
    ) -> None:
        # TODO: WTF???
        code, message = (
            response.data.get("code", -1),
            response.data.get("message", ""),
        )

        if response.status_code == 400:
            raise MaxBotBadRequestError(code, message)
        if response.status_code == 401:
            raise MaxBotUnauthorizedError(code, message)
        if response.status_code == 403:
            raise MaxVotForbiddenError(code, message)
        if response.status_code == 404:
            raise MaxBotNotFoundError(code, message)
        if response.status_code == 405:
            raise MaxBotMethodNotAllowedError(code, message)
        if response.status_code == 429:
            raise MaxBotTooManyRequestsError(code, message)
        if response.status_code == 503:
            raise MaxBotServiceUnavailableError(code, message)

        return await super().handle_error_response(response)
