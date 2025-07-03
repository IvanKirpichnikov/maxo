from collections.abc import Iterable

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.enums.text_fromat import TextFormat
from maxo.kerno.types.types.new_message_link import NewMessageLink
from maxo.kerno.types.types.request_attachments import AttachmentsRequests
from maxo.omit import Omittable


class NewMessageBody(MaxoType):
    text: str | None = None
    attachments: Iterable[AttachmentsRequests] | None = None
    link: NewMessageLink | None = None
    notify: Omittable[bool] = True
    format: TextFormat | None = None
