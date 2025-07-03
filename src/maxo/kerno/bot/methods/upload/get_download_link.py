from retejo.markers import QueryParam
from retejo.method import Method

from maxo.kerno.types.enums.upload_type import UploadType
from maxo.kerno.types.method_results.get_download_link import GetDownloadLinkResult


class GetDownloadLink(Method[GetDownloadLinkResult]):
    __url__ = "uploads"
    __method__ = "post"

    type: QueryParam[UploadType]
