from datetime import datetime

from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class BotStarted(BaseUpdate):
    timestamp: datetime
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None
