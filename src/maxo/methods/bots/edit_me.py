from retejo.markers import Body, Omittable, Omitted
from retejo.method import Method

from maxo.types.bot.bot_command import BotCommand
from maxo.types.bot.me import Me
from maxo.types.request_attachments.payloads import (
    PhotoAttachmentRequestPayload,
)

__all__ = ["EditMe"]


class EditMe(Method[Me]):
    __url__ = "me"
    __method__ = "patch"

    name: Body[Omittable[str | None]] = Omitted()
    description: Body[Omittable[str | None]] = Omitted()
    commands: Body[Omittable[list[BotCommand] | None]] = Omitted()
    photo: Body[PhotoAttachmentRequestPayload | None] = None
