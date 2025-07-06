from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeVar
from typing_extensions import assert_never

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
from maxo.kerno.bot.methods.bots.edit_me import EditMe
from maxo.kerno.bot.methods.bots.get_me import GetMe
from maxo.kerno.bot.methods.chats.add_chat_members import AddChatMembers
from maxo.kerno.bot.methods.chats.delete_chat import DeleteChat
from maxo.kerno.bot.methods.chats.delete_chat_member import DeleteChatMember
from maxo.kerno.bot.methods.chats.delete_pin_message import DeletePinMessage
from maxo.kerno.bot.methods.chats.edit_chat import EditChat
from maxo.kerno.bot.methods.chats.get_chat import GetChat
from maxo.kerno.bot.methods.chats.get_chat_by_link import GetChatByLink
from maxo.kerno.bot.methods.chats.get_chat_members import GetChatMembers
from maxo.kerno.bot.methods.chats.get_chats import GetChats
from maxo.kerno.bot.methods.chats.get_message_pin import GetMessagePin
from maxo.kerno.bot.methods.chats.pin_message import PinMessage
from maxo.kerno.bot.methods.chats.remove_me_chat import RemoveMeChat
from maxo.kerno.bot.methods.chats.revoke_administrator_rights import (
    RevokeAdministratorRights,
)
from maxo.kerno.bot.methods.chats.send_chat_action import SendChatAction
from maxo.kerno.bot.methods.messages.callback_answer import CallbackAnswer
from maxo.kerno.bot.methods.messages.delete_message import DeleteMessage
from maxo.kerno.bot.methods.messages.edit_message import EditMessage
from maxo.kerno.bot.methods.messages.get_message import GetMessage
from maxo.kerno.bot.methods.messages.get_messages import GetMessages
from maxo.kerno.bot.methods.messages.get_video_info import GetVideoInfo
from maxo.kerno.bot.methods.messages.send_message import SendMessage
from maxo.kerno.bot.methods.subscriptions.get_updates import GetUpdates
from maxo.kerno.bot.methods.upload.get_download_link import GetDownloadLink
from maxo.kerno.bot.methods.upload.upload_media import UploadMedia

class WarmingUpType(Enum):
    TYPE = "type"
    METHOD = "method"



@dataclass
class WarmingUpObj:
    tp: Any
    type: WarmingUpType


_types = [
    WarmingUpObj(Attachments, WarmingUpType.TYPE),
    WarmingUpObj(AttachmentsRequests, WarmingUpType.TYPE),
    WarmingUpObj(AudioAttachment, WarmingUpType.TYPE),
    WarmingUpObj(AudioAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(BaseUpdate, WarmingUpType.TYPE),
    WarmingUpObj(BotAdded, WarmingUpType.TYPE),
    WarmingUpObj(BotCommand, WarmingUpType.TYPE),
    WarmingUpObj(BotRemoved, WarmingUpType.TYPE),
    WarmingUpObj(BotStarted, WarmingUpType.TYPE),
    WarmingUpObj(Callback, WarmingUpType.TYPE),
    WarmingUpObj(CallbackKeyboardButton, WarmingUpType.TYPE),
    WarmingUpObj(ChatKeyboardButton, WarmingUpType.TYPE),
    WarmingUpObj(ChatMember, WarmingUpType.TYPE),
    WarmingUpObj(ChatTitileChanged, WarmingUpType.TYPE),
    WarmingUpObj(CommandObject, WarmingUpType.TYPE),
    WarmingUpObj(ContactAttachment, WarmingUpType.TYPE),
    WarmingUpObj(ContactAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(ContactAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(ContactAttachmentRequestPayload, WarmingUpType.TYPE),
    WarmingUpObj(EmphasizedMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(FileAttachment, WarmingUpType.TYPE),
    WarmingUpObj(FileAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(FileAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(GetChatAdministratorsResult, WarmingUpType.TYPE),
    WarmingUpObj(GetChatMembersResult, WarmingUpType.TYPE),
    WarmingUpObj(GetChatResult, WarmingUpType.TYPE),
    WarmingUpObj(GetDownloadLinkResult, WarmingUpType.TYPE),
    WarmingUpObj(GetMessagePinResult, WarmingUpType.TYPE),
    WarmingUpObj(GetMessagesResult, WarmingUpType.TYPE),
    WarmingUpObj(GetUpdatesResult, WarmingUpType.TYPE),
    WarmingUpObj(HeadingMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(HighlightedMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(Image, WarmingUpType.TYPE),
    WarmingUpObj(ImageAttachment, WarmingUpType.TYPE),
    WarmingUpObj(ImageAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(InlineKeyboardAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(InlineKeyboardAttachmentRequestPayload, WarmingUpType.TYPE),
    WarmingUpObj(Keyboard, WarmingUpType.TYPE),
    WarmingUpObj(KeyboardAttachment, WarmingUpType.TYPE),
    WarmingUpObj(KeyboardButtons, WarmingUpType.TYPE),
    WarmingUpObj(KeyboardPayloadAttachment, WarmingUpType.TYPE),
    WarmingUpObj(LinkKeyboardButton, WarmingUpType.TYPE),
    WarmingUpObj(LinkMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(LinkedMessage, WarmingUpType.TYPE),
    WarmingUpObj(LocationAttachment, WarmingUpType.TYPE),
    WarmingUpObj(LocationAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(MarkupElements, WarmingUpType.TYPE),
    WarmingUpObj(MaxoType, WarmingUpType.TYPE),
    WarmingUpObj(Me, WarmingUpType.TYPE),
    WarmingUpObj(MediaAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(MediaAttachmentsRequests, WarmingUpType.TYPE),
    WarmingUpObj(Message, WarmingUpType.TYPE),
    WarmingUpObj(MessageBody, WarmingUpType.TYPE),
    WarmingUpObj(MessageCallback, WarmingUpType.TYPE),
    WarmingUpObj(MessageChatCreated, WarmingUpType.TYPE),
    WarmingUpObj(MessageCreated, WarmingUpType.TYPE),
    WarmingUpObj(MessageEdited, WarmingUpType.TYPE),
    WarmingUpObj(MessageRemoved, WarmingUpType.TYPE),
    WarmingUpObj(MessageStat, WarmingUpType.TYPE),
    WarmingUpObj(MethodResult, WarmingUpType.TYPE),
    WarmingUpObj(MonospacedMarkupElements, WarmingUpType.TYPE),
    WarmingUpObj(NewMessage, WarmingUpType.TYPE),
    WarmingUpObj(NewMessageBody, WarmingUpType.TYPE),
    WarmingUpObj(NewMessageLink, WarmingUpType.TYPE),
    WarmingUpObj(PhotoAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(PhotoAttachmentRequestPayload, WarmingUpType.TYPE),
    WarmingUpObj(Recipient, WarmingUpType.TYPE),
    WarmingUpObj(RequestContactKeyboardButton, WarmingUpType.TYPE),
    WarmingUpObj(RequestGeoLocationKeyboardButton, WarmingUpType.TYPE),
    WarmingUpObj(SendMessageResult, WarmingUpType.TYPE),
    WarmingUpObj(ShareAttachment, WarmingUpType.TYPE),
    WarmingUpObj(ShareAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(ShareAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(StickerAttachment, WarmingUpType.TYPE),
    WarmingUpObj(StickerAttachmentPayload, WarmingUpType.TYPE),
    WarmingUpObj(StickerAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(StickerAttachmentRequestPayload, WarmingUpType.TYPE),
    WarmingUpObj(StrikethroughMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(StrongMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(UnderlineMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(UploadImagePhotoTokenResult, WarmingUpType.TYPE),
    WarmingUpObj(UploadMediaResult, WarmingUpType.TYPE),
    WarmingUpObj(UploadedInfo, WarmingUpType.TYPE),
    WarmingUpObj(User, WarmingUpType.TYPE),
    WarmingUpObj(UserAdded, WarmingUpType.TYPE),
    WarmingUpObj(UserMentionMarkupElement, WarmingUpType.TYPE),
    WarmingUpObj(UserRemoved, WarmingUpType.TYPE),
    WarmingUpObj(VideoAttachment, WarmingUpType.TYPE),
    WarmingUpObj(VideoAttachmentRequest, WarmingUpType.TYPE),
    WarmingUpObj(VideoInfo, WarmingUpType.TYPE),
    WarmingUpObj(VideoThumbnail, WarmingUpType.TYPE),
    WarmingUpObj(VideoUrls, WarmingUpType.TYPE),
]

_methods = [
    WarmingUpObj(SendChatAction, WarmingUpType.METHOD),
    WarmingUpObj(EditMe, WarmingUpType.METHOD),
    WarmingUpObj(GetMe, WarmingUpType.METHOD),
    WarmingUpObj(AddChatMembers, WarmingUpType.METHOD),
    WarmingUpObj(DeleteChat, WarmingUpType.METHOD),
    WarmingUpObj(DeleteChatMember, WarmingUpType.METHOD),
    WarmingUpObj(DeletePinMessage, WarmingUpType.METHOD),
    WarmingUpObj(EditChat, WarmingUpType.METHOD),
    WarmingUpObj(GetChat, WarmingUpType.METHOD),
    WarmingUpObj(GetChatByLink, WarmingUpType.METHOD),
    WarmingUpObj(GetChatMembers, WarmingUpType.METHOD),
    WarmingUpObj(GetChats, WarmingUpType.METHOD),
    WarmingUpObj(GetMessagePin, WarmingUpType.METHOD),
    WarmingUpObj(PinMessage, WarmingUpType.METHOD),
    WarmingUpObj(RemoveMeChat, WarmingUpType.METHOD),
    WarmingUpObj(RevokeAdministratorRights, WarmingUpType.METHOD),
    WarmingUpObj(CallbackAnswer, WarmingUpType.METHOD),
    WarmingUpObj(DeleteMessage, WarmingUpType.METHOD),
    WarmingUpObj(EditMessage, WarmingUpType.METHOD),
    WarmingUpObj(GetMessage, WarmingUpType.METHOD),
    WarmingUpObj(GetMessages, WarmingUpType.METHOD),
    WarmingUpObj(GetVideoInfo, WarmingUpType.METHOD),
    WarmingUpObj(SendMessage, WarmingUpType.METHOD),
    WarmingUpObj(GetUpdates, WarmingUpType.METHOD),
    WarmingUpObj(GetDownloadLink, WarmingUpType.METHOD),
    WarmingUpObj(UploadMedia, WarmingUpType.METHOD),
]

T = TypeVar("T", bound=Retort)


def warming_up_retort(
    retort: T,
    warming_up: WarmingUpType | None = None,
) -> T:
    if warming_up is None:
        return retort

    if warming_up is WarmingUpType.METHOD:
        types = _methods
        retort_method = retort.get_dumper
    elif warming_up is WarmingUpType.TYPE:
        types = _types
        retort_method = retort.get_loader
    else:
        assert_never(warming_up)

    for tp in types:
        retort_method(tp.tp)

    return retort
