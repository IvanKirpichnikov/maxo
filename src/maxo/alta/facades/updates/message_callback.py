from maxo.alta.facades.methods.callback import CallbackMethodsFacade
from maxo.alta.facades.methods.message import MessageMethodsFacade
from maxo.alta.facades.updates.base import BaseUpdateFacade
from maxo.routing.updates.message_callback import MessageCallback
from maxo.types.api.callback import Callback
from maxo.types.api.message import Message


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
