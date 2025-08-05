from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.api.chat_member import ChatMember
from maxo.types.base import MaxoType


class GetChatMembersResult(MaxoType):
    """
    Результат получения участников чата.

    Args:
        members: Список участников чата с информацией о времени последней активности.
        marker: Указатель на следующую страницу данных.

    """

    members: Sequence[ChatMember]
    marker: Omittable[int | None] = Omitted()
