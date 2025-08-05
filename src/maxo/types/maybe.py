from typing import TYPE_CHECKING, Annotated, TypeVar

if TYPE_CHECKING:
    T = TypeVar("T")
    Maybe = Annotated[T, object()]
else:
    class Maybe:
        def __class_getitem__(cls, value):
            return value
