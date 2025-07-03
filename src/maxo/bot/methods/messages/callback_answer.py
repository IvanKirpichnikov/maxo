from retejo.markers import Body, Omittable, Omitted, QueryParam
from retejo.method import Method

from maxo.types.method_results.method import MethodResult
from maxo.types.types.new_message_body import NewMessageBody


class CallbackAnswer(Method[MethodResult]):
    __url__ = "answers"
    __method__ = "post"

    callback_id: QueryParam[str]

    message: Body[NewMessageBody | None] = None
    notification: Body[Omittable[str | None]] = Omitted()
