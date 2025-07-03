from retejo.errors import ClientLibraryError
from retejo.file_obj import FileObj
from retejo.markers import is_defined

from maxo.kerno.bot.bot import Bot
from maxo.kerno.types.method_results.upload_media import UploadMediaResult
from maxo.kerno.types.upload_media import UploadMedia


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
        except ClientLibraryError:
            upload_result = None

        if is_defined(result.token):
            return UploadMediaResult(token=result.token)
        if upload_result is not None:
            return upload_result

        raise RuntimeError
