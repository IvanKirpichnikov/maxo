from dataclasses import dataclass

from maxo.kerno.types.types.chat import Chat
from maxo.kerno.types.types.user import User


@dataclass(frozen=True, slots=True)
class UpdateContext:
    chat: Chat | None = None
    chat_id: int | None = None
    user: User | None = None
    user_id: int | None = None
