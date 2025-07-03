from retejo.markers import Body, Omittable, Omitted, UrlVar
from retejo.method import Method

from maxo.types.chat import Chat
from maxo.types.request_attachments.payloads import (
    PhotoAttachmentRequestPayload,
)

__all__ = ["EditChat"]


class EditChat(Method[Chat]):
    __url__ = "chats/{chat_id}"
    __method__ = "patch"

    chat_id: UrlVar[int]

    icon: Body[PhotoAttachmentRequestPayload | None] = None
    title: Body[Omittable[str | None]] = Omitted()
    pin: Body[Omittable[str | None]] = Omitted()
    notify: Body[Omittable[bool | None]] = True
