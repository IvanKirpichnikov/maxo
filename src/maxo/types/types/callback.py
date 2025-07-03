from datetime import datetime

from maxo.types.base import MaxoType
from maxo.types.types.user import User


class Callback(MaxoType):
    timestamp: datetime
    callback_id: str
    payload: str | None = None
    user: User
