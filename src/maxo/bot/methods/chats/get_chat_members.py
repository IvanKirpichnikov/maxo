from collections.abc import Iterable

from retejo.markers import QueryParam, UrlVar
from retejo.method import Method

from maxo.omit import Omittable, Omitted
from maxo.types.method_results.get_chat_members import GetChatMembersResult


class GetChatMembers(Method[GetChatMembersResult]):
    __url__ = "chats/{chat_id}/members"
    __method__ = "get"

    chat_id: UrlVar[int]

    user_ids: QueryParam[Omittable[Iterable[int] | None]] = Omitted()
    marker: QueryParam[Omittable[int]] = Omitted()
    count: QueryParam[Omittable[int]] = 20
