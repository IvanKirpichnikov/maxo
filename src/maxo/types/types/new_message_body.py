from collections.abc import Iterable

from retejo.markers import Omittable

from maxo.types.base import MaxoType
from maxo.types.enums.text_fromat import TextFormat
from maxo.types.types.new_message_link import NewMessageLink
from maxo.types.types.request_attachments import AttachmentsRequests


class NewMessageBody(MaxoType):
    text: str | None = None
    attachments: Iterable[AttachmentsRequests] | None = None
    link: NewMessageLink | None = None
    notify: Omittable[bool] = True
    format: TextFormat | None = None
