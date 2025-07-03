from datetime import datetime

from maxo.types.types.message import Message
from maxo.types.types.user import User
from maxo.types.updates.base import BaseUpdate


class MessageEdited(BaseUpdate):
    timestamp: datetime
    message: Message

    @property
    def sender(self) -> User:
        return self.message.sender
