from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class ChatTitileChanged(BaseUpdate):
    type = UpdateType.CHAT_TITLE_CHANGED

    timestamp: datetime
    chat_id: int | None = None
    user: User
    title: str | None = None
