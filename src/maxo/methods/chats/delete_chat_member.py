from retejo.markers import QueryParam, UrlVar
from retejo.method import Method

from maxo.omit import Omittable, Omitted
from maxo.types.method_results.method import MethodResult


class DeleteChatMember(Method[MethodResult]):
    __url__ = "chats/{chat_id}/members"
    __method__ = "delete"

    chat_id: UrlVar[int]

    user_id: QueryParam[int]
    block: QueryParam[Omittable[bool]] = Omitted()
