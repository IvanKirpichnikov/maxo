from datetime import datetime

from maxo.types.types.user import User
from maxo.types.updates.base import BaseUpdate


class BotStarted(BaseUpdate):
    timestamp: datetime
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None
