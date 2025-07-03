from datetime import datetime

from maxo.errors.types.message_created import (
    MessageCreatedBodyIsEmptyError,
    MessageCreatedLinkIsEmptyError,
    MessageCreatedStatIsEmptyError,
)
from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.linked_message import LinkedMessage
from maxo.kerno.types.types.message_body import MessageBody
from maxo.kerno.types.types.message_stat import MessageStat
from maxo.kerno.types.types.recipient import Recipient
from maxo.kerno.types.types.user import User
from maxo.omit import Omittable, Omitted


class Message(MaxoType):
    sender: User
    recipient: Recipient
    timestamp: datetime
    link: LinkedMessage | None = None
    body: MessageBody | None = None
    stat: MessageStat | None = None
    url: Omittable[str | None] = Omitted()

    @property
    def unsafe_link(self) -> LinkedMessage:
        if self.link is None:
            raise MessageCreatedLinkIsEmptyError

        return self.link

    @property
    def unsafe_body(self) -> MessageBody:
        if self.body is None:
            raise MessageCreatedBodyIsEmptyError

        return self.body

    @property
    def unsafe_stat(self) -> MessageStat:
        if self.stat is None:
            raise MessageCreatedStatIsEmptyError

        return self.stat
