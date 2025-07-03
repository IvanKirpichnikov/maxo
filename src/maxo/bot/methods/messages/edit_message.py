from collections.abc import Iterable

from retejo.markers import Body, QueryParam
from retejo.method import Method

from maxo.types.enums.text_fromat import TextFormat
from maxo.types.method_results.method import MethodResult
from maxo.types.types.new_message_link import NewMessageLink
from maxo.types.types.request_attachments import AttachmentsRequests


class EditMessage(Method[MethodResult]):
    __url__ = "messages"
    __method__ = "put"

    message_id: QueryParam[str]

    text: Body[str | None] = None
    attachments: Body[Iterable[AttachmentsRequests] | None] = None
    link: Body[NewMessageLink | None] = None
    notify: Body[bool | None] = True
    format: Body[TextFormat | None] = None
