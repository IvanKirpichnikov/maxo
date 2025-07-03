from collections.abc import Sequence

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.message import Message


class GetMessagesResult(MaxoType):
    messages: Sequence[Message]
