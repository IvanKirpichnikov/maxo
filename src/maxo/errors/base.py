from dataclasses import dataclass
from typing import TypeVar

from typing_extensions import dataclass_transform

T = TypeVar("T")


@dataclass_transform(
    frozen_default=True,
)
def error(cls: type[T]) -> type[T]:
    return dataclass(
        slots=True,
        frozen=True,
    )(cls)


@error
class MaxoError(Exception): ...
