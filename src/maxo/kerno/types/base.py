from dataclasses import dataclass
from typing import Any

from typing_extensions import dataclass_transform


@dataclass_transform(
    frozen_default=True,
    kw_only_default=True,
)
class _MaxoTypeMetaClass(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[Any, ...],
        namespace: dict[str, Any],
    ) -> Any:
        class_ = super().__new__(cls, name, bases, namespace)
        if "__slots__" in namespace:
            return class_

        return dataclass(
            slots=True,
            frozen=True,
            kw_only=True,
        )(class_)


class MaxoType(metaclass=_MaxoTypeMetaClass):
    pass
