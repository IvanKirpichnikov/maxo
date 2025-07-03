from collections.abc import Sequence

from retejo.markers import Omittable

from maxo.types.base import MaxoType
from maxo.types.user.chat_member import ChatMember


class GetChatAdministratorsResult(MaxoType):
    members: Sequence[ChatMember]
    marker: Omittable[int | None] = None
