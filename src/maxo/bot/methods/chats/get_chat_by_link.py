from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.types.chat import Chat


class GetChatByLink(Method[Chat]):
    __url__ = "chats/{url}"
    __method__ = "get"

    url: UrlVar[str]
