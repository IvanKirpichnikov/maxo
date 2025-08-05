from datetime import datetime

from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.message import Message
from maxo.types.enums.update_type import UpdateType


class MessageEdited(MaxUpdate):
    type = UpdateType.MESSAGE_EDITED

    timestamp: datetime
    message: Message
