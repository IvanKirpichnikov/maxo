from datetime import datetime

from maxo.errors.types import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.api.callback import Callback
from maxo.types.api.message import Message
from maxo.types.api.user import User
from maxo.types.enums.update_type import UpdateType


class MessageCallback(MaxUpdate):
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

        raise AttributeIsEmptyError(
            obj=self,
            attr="message",
        )

    @property
    def payload(self) -> str | None:
        return self.callback.payload

    @property
    def user(self) -> User:
        return self.callback.user
