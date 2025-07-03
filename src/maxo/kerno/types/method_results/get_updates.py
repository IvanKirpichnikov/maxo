from collections.abc import Sequence

from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.updates import Updates
from maxo.omit import Omittable, Omitted


class GetUpdatesResult(MaxoType):
    updates: Sequence[Updates]
    marker: Omittable[int | None] = Omitted()
