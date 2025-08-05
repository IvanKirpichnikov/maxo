from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.user import User
from maxo.types.enums.update_type import UpdateType


class BotAdded(MaxUpdate):
    type = UpdateType.BOT_ADDED

    timestamp: datetime
    chat_id: int | None = None
    user: User
