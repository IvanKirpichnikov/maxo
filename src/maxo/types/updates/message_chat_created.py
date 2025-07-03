from datetime import datetime

from maxo.types.chat import Chat
from maxo.types.updates.base import BaseUpdate


class MessageChatCreated(BaseUpdate):
    timestamp: datetime
    chat: Chat
    message_id: str | None = None
    start_payload: str | None = None
