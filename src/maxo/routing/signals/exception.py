from typing import Any, Generic, TypeVar

from maxo.routing.signals.base import BaseSignal

_ExceptionT = TypeVar("_ExceptionT", bound=Exception)


class ExceptionEvent(BaseSignal, Generic[_ExceptionT]):
    error: _ExceptionT
    update: Any
