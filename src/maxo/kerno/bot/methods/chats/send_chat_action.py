from retejo.markers import Body, UrlVar
from retejo.method import Method

from maxo.kerno.types.enums.chat_action_type import ChatActionType
from maxo.kerno.types.method_results.method import MethodResult


class SendChatAction(Method[MethodResult]):
    __url__ = "chats/{chat_id}/actions"
    __method__ = "post"

    chat_id: UrlVar[int]
    action: Body[ChatActionType]
