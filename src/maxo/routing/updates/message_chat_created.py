from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.chat import Chat
from maxo.types.enums.update_type import UpdateType


class MessageChatCreated(MaxUpdate):
    type = UpdateType.MESSAGE_CHAT_CREATED

    timestamp: datetime
    chat: Chat
    message_id: str | None = None
    start_payload: str | None = None
