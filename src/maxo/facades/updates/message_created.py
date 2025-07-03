from maxo.facades.methods.message import MessageMethodsFacade
from maxo.facades.updates.base import BaseUpdateFacade
from maxo.types.message.message import Message
from maxo.types.updates.message_created import MessageCreated


class MessageCreatedFacade(
    BaseUpdateFacade[MessageCreated],
    MessageMethodsFacade,
):
    @property
    def message(self) -> Message:
        return self._update.message
