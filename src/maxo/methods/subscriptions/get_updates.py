from collections.abc import Iterable

from retejo import Method
from retejo.markers import QueryParam

from maxo.omit import Omittable, Omitted
from maxo.types.method_results.get_updates import GetUpdatesResult


class GetUpdates(Method[GetUpdatesResult]):
    __url__ = "updates"
    __method__ = "get"

    limit: QueryParam[Omittable[int]] = 100
    timeout: QueryParam[Omittable[int]] = 30
    marker: QueryParam[Omittable[int | None]] = Omitted()
    types: QueryParam[Omittable[Iterable[str]]] = Omitted()
