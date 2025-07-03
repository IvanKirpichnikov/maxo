from maxo.kerno.types.base import MaxoType
from maxo.omit import Omittable, Omitted


class GetDownloadLinkResult(MaxoType):
    url: str
    token: Omittable[str] = Omitted()
