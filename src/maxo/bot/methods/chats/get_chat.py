from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.types.chat import Chat


class GetChat(Method[Chat]):
    __url__ = "chats/{chat_id}"
    __method__ = "get"

    chat_id: UrlVar[int]
