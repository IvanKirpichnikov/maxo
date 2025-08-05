from maxo.alta.upload_media.base import UploadMedia
from maxo.types.enums.upload_type import UploadType


class BufferedUploadMedia(UploadMedia):
    __slots__ = (
        "_data",
        "_file_name",
        "_type",
    )

    def __init__(
        self,
        data: bytes,
        file_name: str,
        type: UploadType,
    ) -> None:
        self._data = data
        self._type = type
        self._file_name = file_name

    @property
    def type(self) -> UploadType:
        return self._type

    @property
    def file_name(self) -> str:
        return self._file_name

    @classmethod
    def image(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.IMAGE)

    @classmethod
    def video(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.VIDEO)

    @classmethod
    def audio(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.AUDIO)

    @classmethod
    def file(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.FILE)

    async def read(self) -> bytes:
        return self._data
