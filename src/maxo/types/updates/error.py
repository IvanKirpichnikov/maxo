from typing import Any, Generic, TypeVar

from maxo.types.updates.base import BaseUpdate

E = TypeVar("E", bound=Exception)


class ErrorEvent(BaseUpdate, Generic[E]):
    error: E
    update: Any
