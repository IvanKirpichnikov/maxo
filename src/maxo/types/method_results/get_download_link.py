from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class GetDownloadLinkResult(MaxoType):
    url: str
    token: Omittable[str] = Omitted()
