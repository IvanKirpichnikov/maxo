from retejo.markers import QueryParam
from retejo.method import Method

from maxo.kerno.types.method_results.method import MethodResult


class DeleteMessage(Method[MethodResult]):
    __url__ = "messages"
    __method__ = "delete"

    message_id: QueryParam[str]
