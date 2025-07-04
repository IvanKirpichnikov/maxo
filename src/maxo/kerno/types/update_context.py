from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.chat import Chat
from maxo.kerno.types.types.user import User


class UpdateContext(MaxoType):
    chat: Chat | None = None
    chat_id: int | None = None
    user: User | None = None
    user_id: int | None = None
