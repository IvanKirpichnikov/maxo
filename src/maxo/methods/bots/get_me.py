from retejo.method import Method

from maxo.types.bot.me import Me

__all__ = ["GetMe"]


class GetMe(Method[Me]):
    __url__ = "me"
    __method__ = "get"
