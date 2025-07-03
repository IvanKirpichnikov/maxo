from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class BotStarted(BaseUpdate):
    type = UpdateType.BOT_STARTED

    timestamp: datetime
    chat_id: int
    user: User
    payload: str | None = None
    user_locale: str | None = None
