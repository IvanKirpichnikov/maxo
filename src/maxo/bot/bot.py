from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import TypeVar

from retejo import Method, bind_method
from retejo.interfaces import AsyncSendableMethod
from typing_extensions import Self

from maxo.bot.api_client import MaxApiClient
from maxo.bot.state import (
    BotState,
    ClosedBotState,
    EmptyBotState,
    InitialBotState,
)
from maxo.methods.bots.edit_me import EditMe
from maxo.methods.bots.get_me import GetMe
from maxo.methods.chats.add_chat_members import AddChatMembers
from maxo.methods.chats.delete_chat import DeleteChat
from maxo.methods.chats.delete_chat_member import DeleteChatMember
from maxo.methods.chats.delete_pin_message import DeletePinMessage
from maxo.methods.chats.edit_chat import EditChat
from maxo.methods.chats.get_chat import GetChat
from maxo.methods.chats.get_chat_by_link import GetChatByLink
from maxo.methods.chats.get_chat_members import GetChatMembers
from maxo.methods.chats.get_chats import GetChats
from maxo.methods.chats.get_message_pin import GetMessagePin
from maxo.methods.chats.pin_message import PinMessage
from maxo.methods.chats.remove_me_chat import RemoveMeChat
from maxo.methods.chats.revoke_administrator_rights import (
    RevokeAdministratorRights,
)
from maxo.methods.chats.send_chat_action import SendChatAction
from maxo.methods.messages.callback_answer import CallbackAnswer
from maxo.methods.messages.delete_message import DeleteMessage
from maxo.methods.messages.edit_message import EditMessage
from maxo.methods.messages.get_message import GetMessage
from maxo.methods.messages.get_messages import GetMessages
from maxo.methods.messages.get_video_info import GetVideoInfo
from maxo.methods.messages.send_message import SendMessage
from maxo.methods.subscriptions.get_updates import GetUpdates
from maxo.methods.upload.get_download_link import GetDownloadLink
from maxo.methods.upload.upload_media import UploadMedia

T = TypeVar("T")


class Bot(
    AsyncSendableMethod,
    AbstractAsyncContextManager["Bot", "None"],
):
    state: BotState

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
