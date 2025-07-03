from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate


class DialogCleared(BaseUpdate):
    type = UpdateType.DIALOG_CLEARED

    timestamp: datetime
    chat_id: int
    user: User
    user_locale: str | None = None
