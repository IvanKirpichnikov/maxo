from retejo.markers import QueryParam
from retejo.method import Method

from maxo.kerno.types.method_results.get_messages_result import GetMessagesResult
from maxo.omit import Omittable, Omitted


class GetMessages(Method[GetMessagesResult]):
    __url__ = "messages"
    __method__ = "get"

    chat_id: QueryParam[Omittable[int]] = Omitted()
    message_ids: QueryParam[Omittable[int | None]] = Omitted()
    from_: QueryParam[Omittable[int]] = Omitted()
    to: QueryParam[Omittable[int]] = Omitted()
    count: QueryParam[Omittable[int]] = 50
