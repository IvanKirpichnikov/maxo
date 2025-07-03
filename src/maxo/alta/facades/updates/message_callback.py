from maxo.alta.facades.methods.callback import CallbackMethodsFacade
from maxo.alta.facades.methods.message import MessageMethodsFacade
from maxo.alta.facades.updates.base import BaseUpdateFacade
from maxo.kerno.types.types.callback import Callback
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.updates.message_callback import MessageCallback


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
