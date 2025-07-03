from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.types.chat_member import ChatMember


class GetChatMembersResult(MaxoType):
    members: Sequence[ChatMember]
    marker: Omittable[int | None] = Omitted()
