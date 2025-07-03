from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.chat_type import ChatType


class Recipient(MaxoType):
    chat_type: ChatType
    user_id: int | None = None
    chat_id: int | None = None
