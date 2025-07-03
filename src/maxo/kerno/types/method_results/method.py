from maxo.kerno.types.base import MaxoType
from maxo.omit import Omittable, Omitted


class MethodResult(MaxoType):
    success: bool
    message: Omittable[str] = Omitted()
