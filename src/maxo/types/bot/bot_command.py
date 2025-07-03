from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class BotCommand(MaxoType):
    name: str
    description: Omittable[str | None] = Omitted()
