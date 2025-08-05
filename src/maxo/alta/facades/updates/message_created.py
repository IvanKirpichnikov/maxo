from maxo.alta.facades.methods.message import MessageMethodsFacade
from maxo.alta.facades.updates.base import BaseUpdateFacade
from maxo.routing.updates.message_created import MessageCreated
from maxo.types.api.message import Message


class MessageCreatedFacade(
    BaseUpdateFacade[MessageCreated],
    MessageMethodsFacade,
):
    @property
    def message(self) -> Message:
        return self._update.message
