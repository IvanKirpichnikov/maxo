from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.routing.updates import Updates
from maxo.types.base import MaxoType


class GetUpdatesResult(MaxoType):
    """
    Результат получения обновлений.

    Args:
        updates: Страница обновлений.
        marker: Указатель на следующую страницу данных.

    """

    updates: Sequence[Updates]
    marker: Omittable[int | None] = Omitted()
