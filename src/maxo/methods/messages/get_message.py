from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.message.message import Message


class GetMessage(Method[Message]):
    __url__ = "messages/{message_id}"
    __method__ = "get"

    message_id: UrlVar[str]
