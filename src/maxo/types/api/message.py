from datetime import datetime

from maxo.errors.types import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.api.linked_message import LinkedMessage
from maxo.types.api.message_body import MessageBody
from maxo.types.api.message_stat import MessageStat
from maxo.types.api.recipient import Recipient
from maxo.types.api.user import User
from maxo.types.base import MaxoType


class Message(MaxoType):
    """
    Сообщение.

    Args:
        sender: Пользователь, отправивший сообщение
        recipient: Получатель сообщения. Может быть пользователем или чатом
        timestamp: Время создания сообщения в формате Unix-time
        link: Пересланное или ответное сообщение
        body:
            Содержимое сообщения. Текст + вложения.
            Может быть null, если сообщение содержит только пересланное сообщение
        stat: Статистика сообщения.
        url: Публичная ссылка на сообщение. Может быть null для диалогов или не публичных чатов

    """

    sender: Omittable[User] = Omitted()
    recipient: Recipient
    timestamp: datetime
    link: Omittable[LinkedMessage | None] = Omitted()
    body: MessageBody | None = None
    stat: Omittable[MessageStat | None] = Omitted()
    url: Omittable[str | None] = Omitted()

    @property
    def unsafe_link(self) -> LinkedMessage:
        if is_defined(self.link):
            return self.link

        raise AttributeIsEmptyError(
            obj=self,
            attr="link",
        )

    @property
    def unsafe_body(self) -> MessageBody:
        if is_defined(self.body):
            return self.body

        raise AttributeIsEmptyError(
            obj=self,
            attr="body",
        )

    @property
    def unsafe_stat(self) -> MessageStat:
        if is_defined(self.stat):
            return self.stat

        raise AttributeIsEmptyError(
            obj=self,
            attr="stat",
        )

