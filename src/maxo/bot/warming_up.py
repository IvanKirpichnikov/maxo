from enum import Enum
from mailbox import Message
from tkinter import Image
from typing import Any, TypeVar, assert_never

from adaptix import Retort

from maxo.bot.method_results.chats.add_chat_administrators import AddChatAdministratorsResult
from maxo.bot.method_results.chats.add_chat_members import AddChatMembersResult
from maxo.bot.method_results.chats.delete_chat import DeleteChatResult
from maxo.bot.method_results.chats.delete_chat_member import DeleteChatMemberResult
from maxo.bot.method_results.chats.delete_me_from_chat import DeleteMeFromChatResult
from maxo.bot.method_results.chats.delete_pin_message import DeletePinMessageResult
from maxo.bot.method_results.chats.get_chat_administrators import GetChatAdministratorsResult
from maxo.bot.method_results.chats.get_chat_members import GetChatMembersResult
from maxo.bot.method_results.chats.get_chats import GetChatsResult
from maxo.bot.method_results.chats.pin_message import PinMessageResult
from maxo.bot.method_results.chats.revoke_administrator_rights import (
    RevokeAdministratorRightsResult,
)
from maxo.bot.method_results.chats.send_chat_action import SendChatActionResult
from maxo.bot.method_results.messages.callback_answer import CallbackAnswerResult
from maxo.bot.method_results.messages.delete_message import DeleteMessageResult
from maxo.bot.method_results.messages.edit_message import EditMessageResult
from maxo.bot.method_results.messages.get_messages import GetMessagesResult
from maxo.bot.method_results.messages.send_message import SendMessageResult
from maxo.bot.method_results.subscriptions.get_updates import GetUpdatesResult
from maxo.bot.method_results.upload.get_download_link import GetDownloadLinkResult
from maxo.bot.method_results.upload.upload_media import (
    UploadImagePhotoTokenResult,
    UploadMediaResult,
)
from maxo.bot.methods.bots.edit_bot_info import EditBotInfo
from maxo.bot.methods.bots.get_bot_info import GetBotInfo
from maxo.bot.methods.chats.add_chat_administrators import AddChatAdministrators
from maxo.bot.methods.chats.add_chat_members import AddChatMembers
from maxo.bot.methods.chats.delete_chat import DeleteChat
from maxo.bot.methods.chats.delete_chat_member import DeleteChatMember
from maxo.bot.methods.chats.delete_me_from_chat import DeleteMeFromChat
from maxo.bot.methods.chats.delete_pin_message import DeletePinMessage
from maxo.bot.methods.chats.edit_chat import EditChat
from maxo.bot.methods.chats.get_chat import GetChat
from maxo.bot.methods.chats.get_chat_administrators import GetChatAdministrators
from maxo.bot.methods.chats.get_chat_by_link import GetChatByLink
from maxo.bot.methods.chats.get_chat_members import GetChatMembers
from maxo.bot.methods.chats.get_chats import GetChats
from maxo.bot.methods.chats.get_me_chat_membership import GetMeChatMembership
from maxo.bot.methods.chats.get_pin_message import GetPinMessage
from maxo.bot.methods.chats.pin_message import PinMessage
from maxo.bot.methods.chats.revoke_administrator_rights import (
    RevokeAdministratorRights,
)
from maxo.bot.methods.chats.send_chat_action import SendChatAction
from maxo.bot.methods.messages.callback_answer import CallbackAnswer
from maxo.bot.methods.messages.delete_message import DeleteMessage
from maxo.bot.methods.messages.edit_message import EditMessage
from maxo.bot.methods.messages.get_message import GetMessage
from maxo.bot.methods.messages.get_messages import GetMessages
from maxo.bot.methods.messages.get_video_info import GetVideoInfo
from maxo.bot.methods.messages.send_message import SendMessage
from maxo.bot.methods.subscriptions.get_updates import GetUpdates
from maxo.bot.methods.upload.get_download_link import GetDownloadLink
from maxo.bot.methods.upload.upload_media import UploadMedia
from maxo.types.api.audio_attachment import AudioAttachment
from maxo.types.api.audio_attachment_request import AudioAttachmentRequest
from maxo.types.api.bot_command import BotCommand
from maxo.types.api.bot_info import BotInfo
from maxo.types.api.callback import Callback
from maxo.types.api.callback_keyboard_button import CallbackKeyboardButton
from maxo.types.api.chat import Chat
from maxo.types.api.chat_admin import ChatAdmin
from maxo.types.api.chat_keyboard_button import ChatKeyboardButton
from maxo.types.api.chat_member import ChatMember
from maxo.types.api.chat_membership import ChatMembership
from maxo.types.api.contact_attachment import ContactAttachment
from maxo.types.api.contact_attachment_payload import ContactAttachmentPayload
from maxo.types.api.contact_attachment_request import ContactAttachmentRequest
from maxo.types.api.contact_attachment_request_payload import ContactAttachmentRequestPayload
from maxo.types.api.file_attachment import FileAttachment
from maxo.types.api.file_attachment_payload import FileAttachmentPayload
from maxo.types.api.file_attachment_request import FileAttachmentRequest
from maxo.types.api.image_attachment import ImageAttachment
from maxo.types.api.image_attachment_request import ImageAttachmentRequest
from maxo.types.api.inline_keyboard_attachment import InlineKeyboardAttachment
from maxo.types.api.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from maxo.types.api.inline_keyboard_attachment_request_payload import (
    InlineKeyboardAttachmentRequestPayload,
)
from maxo.types.api.keyboard import Keyboard
from maxo.types.api.link_keyboard_button import LinkKeyboardButton
from maxo.types.api.linked_message import LinkedMessage
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
from maxo.types.api.media_attachment_payload import MediaAttachmentPayload
from maxo.types.api.message_body import MessageBody
from maxo.types.api.message_keyboard_button import MessageKeyboardButton
from maxo.types.api.message_stat import MessageStat
from maxo.types.api.new_message import NewMessage
from maxo.types.api.new_message_body import NewMessageBody
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.api.open_app_keyboard_button import OpenAppKeyboardButton
from maxo.types.api.photo_attachment_payload import PhotoAttachmentPayload
from maxo.types.api.photo_attachment_request_payload import PhotoAttachmentRequestPayload
from maxo.types.api.recipient import Recipient
from maxo.types.api.request_contact_keyboard_button import RequestContactKeyboardButton
from maxo.types.api.request_geo_location_button import RequestGeoLocationKeyboardButton
from maxo.types.api.share_attachment import ShareAttachment
from maxo.types.api.share_attachment_payload import ShareAttachmentPayload
from maxo.types.api.share_attachment_request import ShareAttachmentRequest
from maxo.types.api.sticker_attachment import StickerAttachment
from maxo.types.api.sticker_attachment_payload import StickerAttachmentPayload
from maxo.types.api.sticker_attachment_request import StickerAttachmentRequest
from maxo.types.api.sticker_attachment_request_payload import StickerAttachmentRequestPayload
from maxo.types.api.uploaded_info import UploadedInfo
from maxo.types.api.user import User
from maxo.types.api.user_with_photo import UserWithPhoto
from maxo.types.api.video_attachment import VideoAttachment
from maxo.types.api.video_attachment_request import VideoAttachmentRequest
from maxo.types.api.video_info import VideoInfo
from maxo.types.api.video_thumbnail import VideoThumbnail
from maxo.types.api.video_urls import VideoUrls


class WarmingUpType(Enum):
    METHOD = "method"
    TYPES = "types"


_types = [
    AudioAttachmentRequest,
    AudioAttachment,
    BotCommand,
    BotInfo,
    CallbackKeyboardButton,
    Callback,
    ChatAdmin,
    ChatKeyboardButton,
    ChatMember,
    ChatMembership,
    Chat,
    ContactAttachmentPayload,
    ContactAttachmentRequestPayload,
    ContactAttachmentRequest,
    ContactAttachment,
    FileAttachmentPayload,
    FileAttachmentRequest,
    FileAttachment,
    ImageAttachmentRequest,
    ImageAttachment,
    Image,
    InlineKeyboardAttachmentRequestPayload,
    InlineKeyboardAttachmentRequest,
    InlineKeyboardAttachment,
    Keyboard,
    LinkKeyboardButton,
    LinkedMessage,
    LocationAttachmentRequest,
    LocationAttachment,
    EmphasizedMarkupElement,
    HeadingMarkupElement,
    HighlightedMarkupElement,
    LinkMarkupElement,
    MonospacedMarkupElements,
    StrikethroughMarkupElement,
    StrongMarkupElement,
    UnderlineMarkupElement,
    UserMentionMarkupElement,
    MediaAttachmentPayload,
    MessageBody,
    MessageKeyboardButton,
    MessageStat,
    Message,
    NewMessageBody,
    NewMessageLink,
    NewMessage,
    OpenAppKeyboardButton,
    PhotoAttachmentPayload,
    PhotoAttachmentRequestPayload,
    Recipient,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
    ShareAttachmentPayload,
    ShareAttachmentRequest,
    ShareAttachment,
    StickerAttachmentPayload,
    StickerAttachmentRequestPayload,
    StickerAttachmentRequest,
    StickerAttachment,
    UploadedInfo,
    UserWithPhoto,
    User,
    VideoAttachmentRequest,
    VideoAttachment,
    VideoInfo,
    VideoThumbnail,
    VideoUrls,
    AddChatAdministratorsResult,
    AddChatMembersResult,
    DeleteChatMemberResult,
    DeleteChatResult,
    DeleteMeFromChatResult,
    DeletePinMessageResult,
    GetChatAdministratorsResult,
    GetChatMembersResult,
    GetChatsResult,
    PinMessageResult,
    RevokeAdministratorRightsResult,
    SendChatActionResult,
    CallbackAnswerResult,
    DeleteMessageResult,
    EditMessageResult,
    GetMessagesResult,
    SendMessageResult,
    GetUpdatesResult,
    GetDownloadLinkResult,
    UploadImagePhotoTokenResult,
    UploadMediaResult,
]


_methods = [
    GetBotInfo,
    EditBotInfo,
    AddChatAdministrators,
    AddChatMembers,
    DeleteChatMember,
    DeleteChat,
    DeleteMeFromChat,
    DeletePinMessage,
    EditChat,
    GetChatAdministrators,
    GetChatByLink,
    GetChatMembers,
    GetChat,
    GetChats,
    GetMeChatMembership,
    GetPinMessage,
    PinMessage,
    RevokeAdministratorRights,
    SendChatAction,
    CallbackAnswer,
    DeleteMessage,
    EditMessage,
    GetMessage,
    GetMessages,
    GetVideoInfo,
    SendMessage,
    GetUpdates,
    GetDownloadLink,
    UploadMedia,
]

_RetortT = TypeVar("_RetortT", bound=Retort)


def warming_up_retort(
    retort: _RetortT,
    warming_up: WarmingUpType | None = None,
) -> _RetortT:
    if warming_up is None:
        return retort

    types: list[Any]
    if warming_up is WarmingUpType.METHOD:
        types = _methods
        retort_method = retort.get_dumper
    elif warming_up is WarmingUpType.TYPES:
        types = _types
        retort_method = retort.get_loader
    else:
        assert_never(warming_up)

    for tp in types:
        retort_method(tp)

    return retort
