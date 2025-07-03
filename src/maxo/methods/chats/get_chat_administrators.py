from retejo.markers import UrlVar
from retejo.method import Method

from maxo.types.method_results.get_chat_administrators import (
    GetChatAdministratorsResult,
)


class GetChatAdministrators(Method[GetChatAdministratorsResult]):
    __url__ = "chats/{chatId}/members/admins"
    __method__ = "get"

    chat_id: UrlVar[int]
