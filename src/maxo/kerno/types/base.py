from dataclasses import dataclass
from typing import Any

from typing_extensions import dataclass_transform


@dataclass_transform(
    eq_default=False,
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
        new_class = super().__new__(cls, name, bases, namespace)
        return dataclass(
            frozen=True,
            eq=False,
            kw_only=True,
        )(new_class)


class MaxoType(metaclass=_MaxoTypeMetaClass):
    pass
