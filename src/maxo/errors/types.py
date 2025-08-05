from typing import Any

from maxo.errors.base import MaxoError, maxo_error


@maxo_error
class AttributeIsEmptyError(MaxoError):
    obj: Any
    attr: str

    def __str__(self) -> str:
        return f"{self.obj.__class__.__name__}.{self.attr} is empty({getattr(self.obj, self.attr)!r})"
