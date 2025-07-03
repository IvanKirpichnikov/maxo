from datetime import datetime

from maxo.types.updates.base import BaseUpdate


class MessageRemoved(BaseUpdate):
    timestamp: datetime
    message_id: str | None = None
    chat_id: str | None = None
    user_id: int | None = None
