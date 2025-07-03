from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.method_results.method import MethodResult


class DeletePinMessage(Method[MethodResult]):
    __url__ = "chats/{chat_id}/pin"
    __method__ = "delete"

    chat_id: UrlVar[int]
