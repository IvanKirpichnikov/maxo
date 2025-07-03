from collections.abc import Iterable

from retejo.markers import Body, UrlVar
from retejo.method import Method

from maxo.types.method_results.method import MethodResult


class AddChatMembers(Method[MethodResult]):
    __url__ = "chats/{chat_id}/members"
    __method__ = "post"

    chat_id: UrlVar[int]

    user_ids: Body[Iterable[int]]
