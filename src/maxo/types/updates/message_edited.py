from datetime import datetime

from maxo.types.message.message import Message
from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class MessageEdited(BaseUpdate):
    timestamp: datetime
    message: Message

    @property
    def sender(self) -> User:
        return self.message.sender
