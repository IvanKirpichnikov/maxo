from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class MethodResult(MaxoType):
    success: bool
    message: Omittable[str] = Omitted()
