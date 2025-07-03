from retejo.markers import UrlVar
from retejo.method import Method

from maxo.kerno.types.method_results.method import MethodResult


class RevokeAdministratorRights(Method[MethodResult]):
    __url__ = "/chats/{chat_id}/members/admins/{user_id}"
    __method__ = "delete"

    chat_id: UrlVar[int]
    user_id: UrlVar[int]
