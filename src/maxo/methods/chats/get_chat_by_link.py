from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.chat import Chat

__all__ = ["GetChatByLink"]


class GetChatByLink(Method[Chat]):
    __url__ = "chats/{url}"
    __method__ = "get"

    url: UrlVar[str]
