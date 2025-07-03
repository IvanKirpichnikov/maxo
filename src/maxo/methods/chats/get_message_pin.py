from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.method_results.get_message_pin import GetMessagePinResult


class GetMessagePin(Method[GetMessagePinResult]):
    __url__ = "chats/{chat_id}/pin"
    __method__ = "get"

    chat_id: UrlVar[int]
