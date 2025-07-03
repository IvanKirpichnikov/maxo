from collections.abc import Iterable
from typing import Any, TypeVar

from adaptix import Retort

from maxo.types.attachments.attachments import (
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
from maxo.types.bot.bot_command import BotCommand
from maxo.types.bot.me import Me
from maxo.types.callback import Callback
from maxo.types.command_object import CommandObject
from maxo.types.image import Image
from maxo.types.keyboard_buttons import (
    CallbackKeyboardButton,
    ChatKeyboardButton,
    Keyboard,
    KeyboardButtons,
    LinkKeyboardButton,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
)
from maxo.types.markup_elements import (
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
from maxo.types.message.linked_message import LinkedMessage
from maxo.types.message.message import Message
from maxo.types.message.message_body import MessageBody
from maxo.types.message.message_stat import MessageStat
from maxo.types.message.new_message import NewMessage
from maxo.types.message.new_message_body import NewMessageBody
from maxo.types.message.new_message_link import NewMessageLink
from maxo.types.method_results.get_chat import GetChatResult
from maxo.types.method_results.get_chat_administrators import (
    GetChatAdministratorsResult,
)
from maxo.types.method_results.get_chat_members import GetChatMembersResult
from maxo.types.method_results.get_download_link import GetDownloadLinkResult
from maxo.types.method_results.get_message_pin import GetMessagePinResult
from maxo.types.method_results.get_messages_result import GetMessagesResult
from maxo.types.method_results.get_updates import GetUpdatesResult
from maxo.types.method_results.method import MethodResult
from maxo.types.method_results.send_message import SendMessageResult
from maxo.types.method_results.upload_media import (
    UploadImagePhotoTokenResult,
    UploadMediaResult,
)
from maxo.types.request_attachments.attachments import (
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
from maxo.types.request_attachments.payloads import (
    ContactAttachmentRequestPayload,
    InlineKeyboardAttachmentRequestPayload,
    PhotoAttachmentRequestPayload,
    StickerAttachmentRequestPayload,
    UploadedInfo,
)
from maxo.types.updates.base import BaseUpdate
from maxo.types.updates.bot_added import BotAdded
from maxo.types.updates.bot_removed import BotRemoved
from maxo.types.updates.bot_started import BotStarted
from maxo.types.updates.chat_title_changed import ChatTitileChanged
from maxo.types.updates.message_callback import MessageCallback
from maxo.types.updates.message_chat_created import MessageChatCreated
from maxo.types.updates.message_created import MessageCreated
from maxo.types.updates.message_edited import MessageEdited
from maxo.types.updates.message_removed import MessageRemoved
from maxo.types.updates.user_added import UserAdded
from maxo.types.updates.user_removed import UserRemoved
from maxo.types.user.chat_member import ChatMember
from maxo.types.user.recipient import Recipient
from maxo.types.user.user import User
from maxo.types.video_info import VideoInfo, VideoUrls

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
