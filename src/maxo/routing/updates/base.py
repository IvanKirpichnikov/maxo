from typing import ClassVar

from maxo.types.base import MaxoType
from maxo.types.enums.update_type import UpdateType


class BaseUpdate(MaxoType):
    pass


class MaxUpdate(BaseUpdate):
    type: ClassVar[UpdateType]
