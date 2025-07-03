from datetime import datetime

from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.chat import Chat
from maxo.kerno.types.updates.base import BaseUpdate


class MessageChatCreated(BaseUpdate):
    type = UpdateType.MESSAGE_CHAT_CREATED

    timestamp: datetime
    chat: Chat
    message_id: str | None = None
    start_payload: str | None = None
