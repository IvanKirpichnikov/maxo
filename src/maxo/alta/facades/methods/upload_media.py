from retejo.http.entities import FileObj

from maxo.alta.upload_media import UploadMedia
from maxo.bot.bot import Bot
from maxo.bot.method_results.upload.upload_media import UploadMediaResult
from maxo.errors.api import RetvalReturnedServerException
from maxo.omit import is_defined


class UploadMediaFacade:
    def __init__(
        self,
        bot: Bot,
        upload_media: UploadMedia,
    ) -> None:
        self._bot = bot
        self._upload_media = upload_media

    async def upload(self) -> UploadMediaResult:
        upload_media = self._upload_media

        result = await self._bot.get_download_link(type=upload_media.type)

        try:
            upload_result = await self._bot.upload_media(
                upload_url=result.url,
                file=FileObj(
                    contents=await upload_media.read(),
                    filename=upload_media.file_name,
                ),
            )
        except RetvalReturnedServerException:
            upload_result = None

        if is_defined(result.token):
            return UploadMediaResult(token=result.token)
        if upload_result is not None:
            return upload_result

        raise RuntimeError
