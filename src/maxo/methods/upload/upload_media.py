from retejo import Method
from retejo.file_obj import FileObj
from retejo.markers import File, UrlVar

from maxo.types.method_results.upload_media import UploadMediaResult


class UploadMedia(Method[UploadMediaResult]):
    __url__ = "{upload_url}"
    __method__ = "post"

    upload_url: UrlVar[str]
    file: File[FileObj]
