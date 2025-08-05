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

__all__ = (
    "AddChatAdministratorsResult",
    "AddChatMembersResult",
    "CallbackAnswerResult",
    "DeleteChatMemberResult",
    "DeleteChatResult",
    "DeleteMeFromChatResult",
    "DeleteMessageResult",
    "DeletePinMessageResult",
    "EditMessageResult",
    "GetChatAdministratorsResult",
    "GetChatMembersResult",
    "GetChatsResult",
    "GetDownloadLinkResult",
    "GetMessagesResult",
    "GetUpdatesResult",
    "PinMessageResult",
    "RevokeAdministratorRightsResult",
    "SendChatActionResult",
    "SendMessageResult",
    "UploadImagePhotoTokenResult",
    "UploadMediaResult",
)
