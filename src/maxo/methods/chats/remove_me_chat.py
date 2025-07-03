from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.method_results.method import MethodResult


class RemoveMeChat(Method[MethodResult]):
    __url__ = "chats/{chat_id}/members/me"
    __method__ = "delete"

    chat_id: UrlVar[int]
