from datetime import datetime

from maxo.errors.types.message_callback import (
    MessageCallbackMessageIsEmptyError,
)
from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.types.callback import Callback
from maxo.kerno.types.types.message import Message
from maxo.kerno.types.types.user import User
from maxo.kerno.types.updates.base import BaseUpdate
from maxo.omit import Omittable, Omitted


class MessageCallback(BaseUpdate):
    type = UpdateType.MESSAGE_CALLBACK

    timestamp: datetime
    callback: Callback
    message: Message | None = None
    user_locale: Omittable[str | None] = Omitted()

    @property
    def callback_id(self) -> str:
        return self.callback.callback_id

    @property
    def unsafe_message(self) -> Message:
        if self.message is not None:
            return self.message

        raise MessageCallbackMessageIsEmptyError

    @property
    def payload(self) -> str | None:
        return self.callback.payload

    @property
    def user(self) -> User:
        return self.callback.user
