from collections.abc import Sequence

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.chat_member import ChatMember
from maxo.omit import Omittable, Omitted


class GetChatMembersResult(MaxoType):
    members: Sequence[ChatMember]
    marker: Omittable[int | None] = Omitted()
