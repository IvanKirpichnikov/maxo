from retejo.http.entities import FileObj
from retejo.http.markers import Form, UrlVar

from maxo.bot.method_results.upload.upload_media import UploadMediaResult
from maxo.bot.methods.base import MaxoMethod


class UploadMedia(MaxoMethod[UploadMediaResult]):
    """
    Загрузка медиа.

    Args:
        upload_url: URL для загрузки медиа.
        file: Загружаемый файл.

    """

    __url__ = "{upload_url}"
    __http_method__ = "post"

    upload_url: UrlVar[str]
    file: Form[FileObj]
