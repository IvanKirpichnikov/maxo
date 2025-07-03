from retejo.markers import QueryParam
from retejo.method import Method

from maxo.omit import Omittable, Omitted
from maxo.types.method_results.get_chat import GetChatResult

__all__ = ["GetChats"]


class GetChats(Method[GetChatResult]):
    __url__ = "chats"
    __method__ = "get"

    count: QueryParam[Omittable[int]] = 50
    marker: QueryParam[Omittable[int | None]] = Omitted()
