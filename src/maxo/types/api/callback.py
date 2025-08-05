from datetime import datetime

from maxo.types.api.user import User
from maxo.types.base import MaxoType


class Callback(MaxoType):
    timestamp: datetime
    callback_id: str
    payload: str | None = None
    user: User
