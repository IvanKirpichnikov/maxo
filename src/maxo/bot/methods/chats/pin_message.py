from retejo.markers import Body, Omittable, UrlVar
from retejo.method import Method

from maxo.types.method_results.method import MethodResult


class PinMessage(Method[MethodResult]):
    __url__ = "chats/{chat_id}/pin"
    __method__ = "put"

    chat_id: UrlVar[int]

    message_id: Body[str]
    notify: Body[Omittable[bool]] = True
