from maxo.types.api.attachments import Attachments
from maxo.types.api.new_message_link import NewMessageLink
from maxo.types.base import MaxoType
from maxo.types.enums.text_fromat import TextFormat


class NewMessage(MaxoType):
    text: str | None = None
    attachments: list[Attachments] | None = None
    link: NewMessageLink | None = None
    notify: bool = True
    format: TextFormat | None = None
