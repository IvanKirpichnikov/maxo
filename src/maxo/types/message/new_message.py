from maxo.enums.text_fromat import TextFormat
from maxo.types.attachments.attachments import Attachments
from maxo.types.base import MaxoType
from maxo.types.message.new_message_link import NewMessageLink

__all__ = ["NewMessage"]


class NewMessage(MaxoType):
    text: str | None = None
    attachments: list[Attachments] | None = None
    link: NewMessageLink | None = None
    notify: bool = True
    format: TextFormat | None = None
