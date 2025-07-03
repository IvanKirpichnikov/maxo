from datetime import datetime

from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class ChatTitileChanged(BaseUpdate):
    timestamp: datetime
    chat_id: int | None = None
    user: User
    title: str | None = None
