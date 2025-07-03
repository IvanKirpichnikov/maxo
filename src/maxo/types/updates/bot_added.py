from datetime import datetime

from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class BotAdded(BaseUpdate):
    timestamp: datetime
    chat_id: int | None = None
    user: User
