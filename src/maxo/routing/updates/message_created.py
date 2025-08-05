from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.message import Message
from maxo.types.enums.update_type import UpdateType


class MessageCreated(MaxUpdate):
    type = UpdateType.MESSAGE_CREATED

    message: Message
    timestamp: datetime
    user_locale: str | None = None
