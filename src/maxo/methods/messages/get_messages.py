from retejo.markers import QueryParam
from retejo.method import Method

from maxo.omit import Omittable, Omitted
from maxo.types.method_results.get_messages_result import GetMessagesResult


class GetMessages(Method[GetMessagesResult]):
    __url__ = "messages"
    __method__ = "get"

    chat_id: QueryParam[Omittable[int]] = Omitted()
    message_ids: QueryParam[Omittable[int | None]] = Omitted()
    from_: QueryParam[Omittable[int]] = Omitted()
    to: QueryParam[Omittable[int]] = Omitted()
    count: QueryParam[Omittable[int]] = 50
