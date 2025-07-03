from datetime import datetime

from maxo.errors.types.message_callback import (
    MessageCallbackMessageIsEmptyError,
)
from maxo.omit import Omittable, Omitted
from maxo.types.callback import Callback
from maxo.types.message.message import Message
from maxo.types.updates.base import BaseUpdate
from maxo.types.user.user import User


class MessageCallback(BaseUpdate):
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
