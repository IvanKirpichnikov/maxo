from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.enums.chat_admin_permission import ChatAdminPermission


class ChatAdmin(MaxoType):
    """
    Администратора чата.

    Args:
        user_id: Идентификатор администратора с правами доступа.
        permissions: Перечень прав пользователя.
        alias:
            Заголовок, который будет показан на клиенте
            Если пользователь администратор или владелец
            и ему не установлено это название, то поле не передается,
            клиенты на своей стороне подменят на "владелец" или "админ".

    """

    user_id: int
    permissions: Sequence[ChatAdminPermission]
    alias: Omittable[str] = Omitted()
