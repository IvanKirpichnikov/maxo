from datetime import datetime

from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class DialogCleared(BaseUpdate):
    timestamp: datetime
    chat_id: int
    user: User
    user_locale: str | None = None
