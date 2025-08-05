from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.user import User
from maxo.types.enums.update_type import UpdateType


class BotStarted(MaxUpdate):
    type = UpdateType.BOT_STARTED

    timestamp: datetime
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None
