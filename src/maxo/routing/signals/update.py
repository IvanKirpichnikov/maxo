from typing import Generic, TypeVar

from maxo.omit import Omittable, Omitted
from maxo.routing.signals.base import BaseSignal
from maxo.routing.updates.base import BaseUpdate

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


class Update(BaseSignal, Generic[_UpdateT]):
    update: _UpdateT
    marker: Omittable[int | None] = Omitted()
