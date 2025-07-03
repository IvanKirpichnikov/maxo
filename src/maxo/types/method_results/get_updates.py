from collections.abc import Sequence

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.updates import Updates


class GetUpdatesResult(MaxoType):
    updates: Sequence[Updates]
    marker: Omittable[int | None] = Omitted()
