import time
from types import TracebackType
from typing import Self, TypeVar

from retejo.core.method_binder import bind_method

from maxo.bot.api_client import MaxApiClient
from maxo.bot.methods.base import MaxoMethod
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
from maxo.bot.state import (
    BotState,
    ClosedBotState,
    EmptyBotState,
    InitialBotState,
)
from maxo.types.base import MaxoType

_MethodResultT = TypeVar("_MethodResultT", bound=MaxoType)


class Bot:
    _state: BotState

    __slots__ = ("_state", "_token", "_warming_up")

    def __init__(
        self,
        token: str,
        warming_up: bool = True,
    ) -> None:
        self._token = token
        self._warming_up = warming_up

        self._state = EmptyBotState()

    @property
    def state(self) -> BotState:
        return self._state

    async def start(self) -> None:
        if self.state.started:
            return None

        time.perf_counter()
        api_client = MaxApiClient(self._token, self._warming_up)
        info = await api_client.send_method(GetBotInfo())
        self._state = InitialBotState(
            info=info,
            api_client=api_client,
        )

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.state.api_client.close()

    async def send_method(
        self,
        method: MaxoMethod[_MethodResultT],
    ) -> _MethodResultT:
        return await self.state.api_client.send_method(method)

    async def close(self) -> None:
        if self.state.closed or not self.state.started:
            return None

        await self.state.api_client.close()
        self._state = ClosedBotState()

    # Subscriptions

    get_updates = bind_method(GetUpdates)

    # Bots

    get_bot_info = bind_method(GetBotInfo)
    edit_bot_info = bind_method(EditBotInfo)

    # Chats

    get_chats = bind_method(GetChats)
    get_chat_by_link = bind_method(GetChatByLink)
    get_chat = bind_method(GetChat)
    edit_chat = bind_method(EditChat)
    delete_chat = bind_method(DeleteChat)

    send_chat_action = bind_method(SendChatAction)

    get_pin_message = bind_method(GetPinMessage)
    pin_message = bind_method(PinMessage)
    delete_pin_message = bind_method(DeletePinMessage)

    get_me_chat_membership = bind_method(GetMeChatMembership)
    remove_me_from_chat = bind_method(DeleteMeFromChat)

    get_chat_administrators = bind_method(GetChatAdministrators)
    add_chat_administrators = bind_method(AddChatAdministrators)
    revoke_administrator_rights = bind_method(RevokeAdministratorRights)

    get_chat_members = bind_method(GetChatMembers)
    add_chat_members = bind_method(AddChatMembers)
    delete_chat_member = bind_method(DeleteChatMember)

    # uploads

    get_download_link = bind_method(GetDownloadLink)
    upload_media = bind_method(UploadMedia)

    # messages
    get_messages = bind_method(GetMessages)
    send_message = bind_method(SendMessage)
    edit_message = bind_method(EditMessage)
    get_message = bind_method(GetMessage)
    delete_message = bind_method(DeleteMessage)

    get_video_info = bind_method(GetVideoInfo)

    callback_answer = bind_method(CallbackAnswer)
