from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class MessageCreated(BaseUpdate):
    type = UpdateType.MESSAGE_CREATED

    message: Message
    timestamp: datetime
    user_locale: str | None = None

    @property
    def sender(self) -> User:
        return self.message.sender
