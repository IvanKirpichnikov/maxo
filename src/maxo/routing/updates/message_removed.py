from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.enums.update_type import UpdateType


class MessageRemoved(MaxUpdate):
    type = UpdateType.MESSAGE_REMOVED

    timestamp: datetime
    message_id: str | None = None
    chat_id: str | None = None
    user_id: int | None = None
