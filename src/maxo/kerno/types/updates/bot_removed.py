from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class BotRemoved(BaseUpdate):
    type = UpdateType.BOT_REMOVED

    timestamp: datetime
    chat_id: int | None = None
    user: User
