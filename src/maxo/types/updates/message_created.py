from datetime import datetime

from maxo.types.message.message import Message
from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class MessageCreated(BaseUpdate):
    message: Message
    timestamp: datetime
    user_locale: str | None = None

    @property
    def sender(self) -> User:
        return self.message.sender
