from datetime import datetime

from adaptix import P, Retort, as_sentinel, dumper, loader
from retejo.errors import ServerError
from retejo.integrations.adaptix._omit_provider import OmitOmittedFieldProvider
from retejo.integrations.adaptix.aiohttp import AiohttpAdaptixClient
from retejo.integrations.common.base import MarkersFactorties
from retejo.interfaces import Response
from retejo.markers import (
    BodyMarker,
    HeaderMarker,
    Omitted,
    QueryParamMarker,
    UrlVarMarker,
)

from maxo._adaptix.has_tag_provider import has_tag_provider
from maxo.errors.api import (
    MaxBotBadRequestError,
    MaxBotMethodNotAllowedError,
    MaxBotNotFoundError,
    MaxBotServiceUnavailableError,
    MaxBotTooManyRequestsError,
    MaxBotUnauthorizedError,
    MaxVotForbiddenError,
)
from maxo.kerno.bot.warming_up import warming_up_retort
from maxo.kerno.types.enums.attachment_request_type import AttachmentRequestType
from maxo.kerno.types.enums.attachment_type import AttachmentType
from maxo.kerno.types.enums.keyboard_button_type import KeyboardButtonType
from maxo.kerno.types.enums.markup_element_type import MarkupElementType
from maxo.kerno.types.types.attachments import (
    AudioAttachment,
    ContactAttachment,
    FileAttachment,
    ImageAttachment,
    KeyboardAttachment,
    LocationAttachment,
    ShareAttachment,
    StickerAttachment,
    VideoAttachment,
)
from maxo.kerno.types.types.keyboard_buttons import (
    CallbackKeyboardButton,
    ChatKeyboardButton,
    LinkKeyboardButton,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
)
from maxo.kerno.types.types.markup_elements import (
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
from maxo.kerno.types.types.request_attachments import (
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
from maxo.kerno.types.updates.bot_added import BotAdded
from maxo.kerno.types.updates.bot_removed import BotRemoved
from maxo.kerno.types.updates.bot_started import BotStarted
from maxo.kerno.types.updates.chat_title_changed import ChatTitileChanged
from maxo.kerno.types.updates.dialog_cleared import DialogCleared
from maxo.kerno.types.updates.message_callback import MessageCallback
from maxo.kerno.types.updates.message_chat_created import MessageChatCreated
from maxo.kerno.types.updates.message_created import MessageCreated
from maxo.kerno.types.updates.message_edited import MessageEdited
from maxo.kerno.types.updates.message_removed import MessageRemoved
from maxo.kerno.types.updates.user_added import UserAdded
from maxo.kerno.types.updates.user_removed import UserRemoved

_has_tag_providers = (
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
    has_tag_provider(DialogCleared, "update_type", "dialog_cleared"),
    # ---> AttachmentType <---
    has_tag_provider(AudioAttachment, "type", AttachmentType.AUDIO),
    has_tag_provider(ContactAttachment, "type", AttachmentType.CONTACT),
    has_tag_provider(FileAttachment, "type", AttachmentType.FILE),
    has_tag_provider(ImageAttachment, "type", AttachmentType.IMAGE),
    has_tag_provider(KeyboardAttachment, "type", AttachmentType.INLINE_KEYBOARD),
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
)


class MaxApiClient(AiohttpAdaptixClient):
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

    def init_markers_factories(self) -> MarkersFactorties[Retort]:
        # markers_factories = super().init_markers_factories()
        base_recipe = (
            *_has_tag_providers,
            as_sentinel(Omitted),
            OmitOmittedFieldProvider(),
            dumper(P[datetime], lambda x: x.timestamp() * 1000),
        )
        markers_factories: MarkersFactorties[Retort] = {}

        common_retort = warming_up_retort(Retort(recipe=base_recipe), self._warming_up)
        markers_factories[BodyMarker] = common_retort
        markers_factories[UrlVarMarker] = common_retort
        markers_factories[HeaderMarker] = common_retort
        markers_factories[QueryParamMarker] = common_retort.extend(recipe=[dumper(P[None], lambda x: "null")])

        return markers_factories

    def init_response_factory(self) -> Retort:
        # retort = super().init_response_factory()
        return warming_up_retort(
            Retort(
                recipe=(
                    *_has_tag_providers,
                    loader(P[datetime], lambda x: datetime.fromtimestamp(x / 1000)),
                    as_sentinel(Omitted),
                    OmitOmittedFieldProvider(),
                ),
            ),
            self._warming_up,
        )

    async def _handle_error_response(self, response: Response) -> None:
        code, message = (
            response.data.get("code", ""),
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
        raise ServerError(response.status_code)
