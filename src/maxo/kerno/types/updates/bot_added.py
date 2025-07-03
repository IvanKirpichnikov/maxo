from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class BotAdded(BaseUpdate):
    type = UpdateType.BOT_ADDED

    timestamp: datetime
    chat_id: int | None = None
    user: User
