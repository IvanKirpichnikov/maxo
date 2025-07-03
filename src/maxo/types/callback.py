from datetime import datetime

from maxo.types.base import MaxoType
from maxo.types.user.user import User

__all__ = ["Callback"]


class Callback(MaxoType):
    timestamp: datetime
    callback_id: str
    payload: str | None = None
    user: User
