from types import TracebackType
from typing import TypeVar

from retejo import Method, bind_method
from typing_extensions import Self

from maxo.kerno.bot.api_client import MaxApiClient
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
from maxo.kerno.bot.state import (
    BotState,
    ClosedBotState,
    EmptyBotState,
    InitialBotState,
)

T = TypeVar("T")


class Bot:
    state: BotState

    __slots__ = ("_token", "_warming_up", "state")

    def __init__(
        self,
        token: str,
        warming_up: bool = False,
    ) -> None:
        self._token = token
        self._warming_up = warming_up

        self.state = EmptyBotState()

    async def start(self) -> None:
        if self.state.started:
            return None

        api_client = MaxApiClient(self._token, self._warming_up)
        me = await api_client.send_method(GetMe())
        self.state = InitialBotState(
            me=me,
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
        method: Method[T],
    ) -> T:
        return await self.state.api_client.send_method(method)

    async def close(self) -> None:
        if self.state.closed or not self.state.started:
            return None

        await self.state.api_client.close()
        self.state = ClosedBotState()

    # Subscriptions

    get_updates = bind_method(GetUpdates)

    # Bots

    get_me = bind_method(GetMe)
    edit_me = bind_method(EditMe)

    # Chats

    get_chats = bind_method(GetChats)
    get_chat = bind_method(GetChat)
    get_chat_by_link = bind_method(GetChatByLink)
    edit_chat = bind_method(EditChat)
    delete_chat = bind_method(DeleteChat)

    send_chat_action = bind_method(SendChatAction)

    get_message_pin = bind_method(GetMessagePin)
    pin_message = bind_method(PinMessage)
    delete_pin_message = bind_method(DeletePinMessage)

    remove_me_chat = bind_method(RemoveMeChat)

    revoke_administrator_rights = bind_method(RevokeAdministratorRights)

    get_chat_members = bind_method(GetChatMembers)
    add_chat_members = bind_method(AddChatMembers)
    delete_chat_member = bind_method(DeleteChatMember)

    # uploads

    get_download_link = bind_method(GetDownloadLink)
    upload_media = bind_method(UploadMedia)

    # messages
    get_messages = bind_method(GetMessages)
    get_message = bind_method(GetMessage)
    send_message = bind_method(SendMessage)
    edit_message = bind_method(EditMessage)
    delete_message = bind_method(DeleteMessage)

    get_video_info = bind_method(GetVideoInfo)

    callback_answer = bind_method(CallbackAnswer)
