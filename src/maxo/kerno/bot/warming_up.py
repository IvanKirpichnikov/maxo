from collections.abc import Iterable
from typing import Any, TypeVar

from adaptix import Retort

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.command_object import CommandObject
from maxo.kerno.types.image import Image
from maxo.kerno.types.method_results.get_chat import GetChatResult
from maxo.kerno.types.method_results.get_chat_administrators import (
    GetChatAdministratorsResult,
)
from maxo.kerno.types.method_results.get_chat_members import GetChatMembersResult
from maxo.kerno.types.method_results.get_download_link import GetDownloadLinkResult
from maxo.kerno.types.method_results.get_message_pin import GetMessagePinResult
from maxo.kerno.types.method_results.get_messages_result import GetMessagesResult
from maxo.kerno.types.method_results.get_updates import GetUpdatesResult
from maxo.kerno.types.method_results.method import MethodResult
from maxo.kerno.types.method_results.send_message import SendMessageResult
from maxo.kerno.types.method_results.upload_media import (
    UploadImagePhotoTokenResult,
    UploadMediaResult,
)
from maxo.kerno.types.types.attachments import (
    Attachments,
    AudioAttachment,
    ContactAttachment,
    FileAttachment,
    ImageAttachment,
    KeyboardAttachment,
    LocationAttachment,
    ShareAttachment,
    StickerAttachment,
    VideoAttachment,
    VideoThumbnail,
)
from maxo.kerno.types.types.callback import Callback
from maxo.kerno.types.types.chat_member import ChatMember
from maxo.kerno.types.types.keyboard_buttons import (
    CallbackKeyboardButton,
    ChatKeyboardButton,
    Keyboard,
    KeyboardButtons,
    LinkKeyboardButton,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
)
from maxo.kerno.types.types.linked_message import LinkedMessage
from maxo.kerno.types.types.markup_elements import (
    EmphasizedMarkupElement,
    HeadingMarkupElement,
    HighlightedMarkupElement,
    LinkMarkupElement,
    MarkupElements,
    MonospacedMarkupElements,
    StrikethroughMarkupElement,
    StrongMarkupElement,
    UnderlineMarkupElement,
    UserMentionMarkupElement,
)
from maxo.kerno.types.types.me import BotCommand, Me
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.types.message_body import MessageBody
from maxo.kerno.types.types.message_stat import MessageStat
from maxo.kerno.types.types.new_message import NewMessage
from maxo.kerno.types.types.new_message_body import NewMessageBody
from maxo.kerno.types.types.new_message_link import NewMessageLink
from maxo.kerno.types.types.payload_attachments import (
    ContactAttachmentPayload,
    FileAttachmentPayload,
    KeyboardPayloadAttachment,
    MediaAttachmentPayload,
    PhotoAttachmentPayload,
    ShareAttachmentPayload,
    StickerAttachmentPayload,
)
from maxo.kerno.types.types.payload_request_attachments import (
    ContactAttachmentRequestPayload,
    InlineKeyboardAttachmentRequestPayload,
    PhotoAttachmentRequestPayload,
    StickerAttachmentRequestPayload,
    UploadedInfo,
)
from maxo.kerno.types.types.recipient import Recipient
from maxo.kerno.types.types.request_attachments import (
    AttachmentsRequests,
    AudioAttachmentRequest,
    ContactAttachmentRequest,
    FileAttachmentRequest,
    ImageAttachmentRequest,
    InlineKeyboardAttachmentRequest,
    LocationAttachmentRequest,
    MediaAttachmentsRequests,
    ShareAttachmentRequest,
    StickerAttachmentRequest,
    VideoAttachmentRequest,
)
from maxo.kerno.types.types.user import User
from maxo.kerno.types.types.video_info import VideoInfo, VideoUrls
from maxo.kerno.types.updates.base import BaseUpdate
from maxo.kerno.types.updates.bot_added import BotAdded
from maxo.kerno.types.updates.bot_removed import BotRemoved
from maxo.kerno.types.updates.bot_started import BotStarted
from maxo.kerno.types.updates.chat_title_changed import ChatTitileChanged
from maxo.kerno.types.updates.message_callback import MessageCallback
from maxo.kerno.types.updates.message_chat_created import MessageChatCreated
from maxo.kerno.types.updates.message_created import MessageCreated
from maxo.kerno.types.updates.message_edited import MessageEdited
from maxo.kerno.types.updates.message_removed import MessageRemoved
from maxo.kerno.types.updates.user_added import UserAdded
from maxo.kerno.types.updates.user_removed import UserRemoved

types: Iterable[Any] = [
    Attachments,
    AttachmentsRequests,
    AudioAttachment,
    AudioAttachmentRequest,
    BaseUpdate,
    BotAdded,
    BotCommand,
    BotRemoved,
    BotStarted,
    Callback,
    CallbackKeyboardButton,
    ChatKeyboardButton,
    ChatMember,
    ChatTitileChanged,
    CommandObject,
    ContactAttachment,
    ContactAttachmentPayload,
    ContactAttachmentRequest,
    ContactAttachmentRequestPayload,
    EmphasizedMarkupElement,
    FileAttachment,
    FileAttachmentPayload,
    FileAttachmentRequest,
    GetChatAdministratorsResult,
    GetChatMembersResult,
    GetChatResult,
    GetDownloadLinkResult,
    GetMessagePinResult,
    GetMessagesResult,
    GetUpdatesResult,
    HeadingMarkupElement,
    HighlightedMarkupElement,
    Image,
    ImageAttachment,
    ImageAttachmentRequest,
    InlineKeyboardAttachmentRequest,
    InlineKeyboardAttachmentRequestPayload,
    Keyboard,
    KeyboardAttachment,
    KeyboardButtons,
    KeyboardPayloadAttachment,
    LinkKeyboardButton,
    LinkMarkupElement,
    LinkedMessage,
    LocationAttachment,
    LocationAttachmentRequest,
    MarkupElements,
    MaxoType,
    Me,
    MediaAttachmentPayload,
    MediaAttachmentsRequests,
    Message,
    MessageBody,
    MessageCallback,
    MessageChatCreated,
    MessageCreated,
    MessageEdited,
    MessageRemoved,
    MessageStat,
    MethodResult,
    MonospacedMarkupElements,
    NewMessage,
    NewMessageBody,
    NewMessageLink,
    PhotoAttachmentPayload,
    PhotoAttachmentRequestPayload,
    Recipient,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
    SendMessageResult,
    ShareAttachment,
    ShareAttachmentPayload,
    ShareAttachmentRequest,
    StickerAttachment,
    StickerAttachmentPayload,
    StickerAttachmentRequest,
    StickerAttachmentRequestPayload,
    StrikethroughMarkupElement,
    StrongMarkupElement,
    UnderlineMarkupElement,
    UploadImagePhotoTokenResult,
    UploadMediaResult,
    UploadedInfo,
    User,
    UserAdded,
    UserMentionMarkupElement,
    UserRemoved,
    VideoAttachment,
    VideoAttachmentRequest,
    VideoInfo,
    VideoThumbnail,
    VideoUrls,
]

T = TypeVar("T", bound=Retort)


def warming_up_retort(
    retort: T,
    warming_up: bool,
) -> T:
    if not warming_up:
        return retort

    for type in types:
        retort.get_loader(type)
        retort.get_dumper(type)

    return retort
