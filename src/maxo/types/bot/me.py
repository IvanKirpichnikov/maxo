from datetime import datetime

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.bot.bot_command import BotCommand


class Me(MaxoType):
    user_id: int
    first_name: str
    last_name: Omittable[str] = Omitted()
    username: str
    is_bot: bool
    last_activity_time: datetime
    description: Omittable[str | None] = Omitted()
    avatar_url: Omittable[str] = Omitted()
    full_avatar_url: Omittable[str] = Omitted()
    commands: Omittable[list[BotCommand] | None] = Omitted()
