from retejo.markers import QueryParam
from retejo.method import Method

from maxo.enums.upload_type import UploadType
from maxo.types.method_results.get_download_link import GetDownloadLinkResult


class GetDownloadLink(Method[GetDownloadLinkResult]):
    __url__ = "uploads"
    __method__ = "post"

    type: QueryParam[UploadType]
