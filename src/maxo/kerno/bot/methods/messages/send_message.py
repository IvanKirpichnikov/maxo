from collections.abc import Sequence

from retejo.markers import Body, Omittable, Omitted, QueryParam
from retejo.method import Method

from maxo.kerno.types.enums.text_fromat import TextFormat
from maxo.kerno.types.method_results.send_message import SendMessageResult
from maxo.kerno.types.types.new_message_link import NewMessageLink
from maxo.kerno.types.types.request_attachments import AttachmentsRequests


class SendMessage(Method[SendMessageResult]):
    __url__ = "messages"
    __method__ = "post"

    user_id: QueryParam[Omittable[int]] = Omitted()
    chat_id: QueryParam[Omittable[int]] = Omitted()
    disable_link_preview: QueryParam[Omittable[bool]] = Omitted()

    text: Body[str | None] = None
    attachments: Body[Sequence[AttachmentsRequests] | None] = None
    link: Body[NewMessageLink | None] = None
    notify: Body[Omittable[bool]] = True
    format: Body[TextFormat | None] = None
