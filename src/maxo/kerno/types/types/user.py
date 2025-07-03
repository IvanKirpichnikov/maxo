from datetime import datetime

from maxo.kerno.types.base import MaxoType
from maxo.omit import Omittable, Omitted


class User(MaxoType):
    user_id: int
    first_name: str
    last_name: Omittable[str] = Omitted()
    username: str | None = None
    is_bot: bool
    last_activity_time: datetime
    description: Omittable[str | None] = Omitted()
    avatar_url: Omittable[str] = Omitted()
    full_avatar_url: Omittable[str] = Omitted()
