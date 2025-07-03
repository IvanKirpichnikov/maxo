from datetime import datetime

from maxo.types.types.user import User
from maxo.types.updates.base import BaseUpdate


class BotRemoved(BaseUpdate):
    timestamp: datetime
    chat_id: int | None = None
    user: User
