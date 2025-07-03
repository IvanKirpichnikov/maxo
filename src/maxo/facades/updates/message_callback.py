from maxo.facades.methods.callback import CallbackMethodsFacade
from maxo.facades.methods.message import MessageMethodsFacade
from maxo.facades.updates.base import BaseUpdateFacade
from maxo.types.callback import Callback
from maxo.types.message.message import Message
from maxo.types.updates.message_callback import MessageCallback


class MessageCallbackFacade(
    BaseUpdateFacade[MessageCallback],
    MessageMethodsFacade,
    CallbackMethodsFacade,
):
    @property
    def message(self) -> Message:
        return self._update.unsafe_message

    @property
    def callback(self) -> Callback:
        return self._update.callback
