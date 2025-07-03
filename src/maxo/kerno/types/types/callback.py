from datetime import datetime

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.user import User


class Callback(MaxoType):
    timestamp: datetime
    callback_id: str
    payload: str | None = None
    user: User
