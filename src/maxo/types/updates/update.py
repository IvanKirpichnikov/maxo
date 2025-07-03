from typing import Generic, TypeVar

from maxo.types.updates.base import BaseUpdate

U = TypeVar("U", bound=BaseUpdate)


class Update(BaseUpdate, Generic[U]):
    update: U
    marker: int | None = None
