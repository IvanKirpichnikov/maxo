from collections.abc import Sequence

from maxo.types.base import MaxoType
from maxo.types.message.message import Message


class GetMessagesResult(MaxoType):
    messages: Sequence[Message]
