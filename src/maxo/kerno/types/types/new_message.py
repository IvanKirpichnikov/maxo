from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.text_fromat import TextFormat
from maxo.kerno.types.types.attachments import Attachments
from maxo.kerno.types.types.new_message_link import NewMessageLink


class NewMessage(MaxoType):
    text: str | None = None
    attachments: list[Attachments] | None = None
    link: NewMessageLink | None = None
    notify: bool = True
    format: TextFormat | None = None
