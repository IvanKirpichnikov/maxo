from retejo.markers import Body, Omittable, Omitted
from retejo.method import Method

from maxo.types.types.me import BotCommand, Me
from maxo.types.types.payload_request_attachments import (
    PhotoAttachmentRequestPayload,
)


class EditMe(Method[Me]):
    __url__ = "me"
    __method__ = "patch"

    name: Body[Omittable[str | None]] = Omitted()
    description: Body[Omittable[str | None]] = Omitted()
    commands: Body[Omittable[list[BotCommand] | None]] = Omitted()
    photo: Body[PhotoAttachmentRequestPayload | None] = None
