from maxo.enums.chat_type import ChatType
from maxo.types.base import MaxoType

__all__ = ["Recipient"]


class Recipient(MaxoType):
    chat_type: ChatType
    user_id: int | None = None
    chat_id: int | None = None
