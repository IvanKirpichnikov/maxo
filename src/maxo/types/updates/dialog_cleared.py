from datetime import datetime

from maxo.types.types.user import User
from maxo.types.updates.base import BaseUpdate


class DialogCleared(BaseUpdate):
    timestamp: datetime
    chat_id: int
    user: User
    user_locale: str | None = None
