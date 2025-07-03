from retejo.method import Method

from maxo.kerno.types.types.me import Me


class GetMe(Method[Me]):
    __url__ = "me"
    __method__ = "get"
