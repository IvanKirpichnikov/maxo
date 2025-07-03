from datetime import datetime

from maxo.types.types.message import Message
from maxo.types.types.user import User
from maxo.types.updates.base import BaseUpdate


class MessageCreated(BaseUpdate):
    message: Message
    timestamp: datetime
    user_locale: str | None = None

    @property
    def sender(self) -> User:
        return self.message.sender
