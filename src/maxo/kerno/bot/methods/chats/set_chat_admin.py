from retejo.markers import UrlVar
from retejo.method import Method

from maxo.kerno.types.method_results.method import MethodResult


# TODO: fill
class SetChatAdmin(Method[MethodResult]):
    __url__ = "chats/{chat_id}/members/admins"
    __method__ = "post"

    chat_id: UrlVar[int]
