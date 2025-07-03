from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.method_results.method import MethodResult


class DeleteChat(Method[MethodResult]):
    __url__ = "chats/{chat_id}"
    __method__ = "delete"

    chat_id: UrlVar[int]
