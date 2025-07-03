from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.updates.base import BaseUpdate


class MessageRemoved(BaseUpdate):
    type = UpdateType.MESSAGE_REMOVED

    timestamp: datetime
    message_id: str | None = None
    chat_id: str | None = None
    user_id: int | None = None
