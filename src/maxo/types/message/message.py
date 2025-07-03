from datetime import datetime

from maxo.errors.types.message_created import (
    MessageCreatedBodyIsEmptyError,
    MessageCreatedLinkIsEmptyError,
    MessageCreatedStatIsEmptyError,
)
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.message.linked_message import LinkedMessage
from maxo.types.message.message_body import MessageBody
from maxo.types.message.message_stat import MessageStat
from maxo.types.user.recipient import Recipient
from maxo.types.user.user import User


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
