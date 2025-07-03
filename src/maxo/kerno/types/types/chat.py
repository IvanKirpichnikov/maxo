from datetime import datetime
from typing import Any

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.chat_status import ChatStatusType
from maxo.kerno.types.enums.chat_type import ChatType
from maxo.kerno.types.image import Image
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.types.user import User
from maxo.omit import Omittable, Omitted


class Chat(MaxoType):
    chat_id: int
    type: ChatType
    status: ChatStatusType
    title: str | None = None
    icon: Image | None = None
    last_event_time: datetime
    participants_count: int
    owner_id: Omittable[int | None] = Omitted()
    participants: Omittable[Any | None] = Omitted()
    is_public: bool
    link: Omittable[str | None] = Omitted()
    description: str | None = None
    dialog_with_user: User | None = None
    messages_count: Omittable[int | None] = Omitted()
    chat_message_id: Omittable[str | None] = Omitted()
    pinned_message: Message | None = None
