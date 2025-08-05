from retejo.http.markers import UrlVar

from maxo.bot.method_results.chats.revoke_administrator_rights import (
    RevokeAdministratorRightsResult,
)
from maxo.bot.methods.base import MaxoMethod


class RevokeAdministratorRights(MaxoMethod[RevokeAdministratorRightsResult]):
    """
    Отменить права администратора.

    Отменяет права администратора у пользователя в чате, лишая его административных привилегий.

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/members/admins/-userId-

    Args:
        chat_id: ID чата.
        user_id: Идентификатор пользователя.

    """

    __url__ = "/chats/{chat_id}/members/admins/{user_id}"
    __http_method__ = "delete"

    chat_id: UrlVar[int]
    user_id: UrlVar[int]
