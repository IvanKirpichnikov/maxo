from retejo.markers import QueryParam, UrlVar
from retejo.method import Method

from maxo.kerno.types.method_results.method import MethodResult
from maxo.omit import Omittable, Omitted


class DeleteChatMember(Method[MethodResult]):
    __url__ = "chats/{chat_id}/members"
    __method__ = "delete"

    chat_id: UrlVar[int]

    user_id: QueryParam[int]
    block: QueryParam[Omittable[bool]] = Omitted()
