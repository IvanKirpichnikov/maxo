from abc import ABC, abstractmethod

from maxo.types.enums.upload_type import UploadType


class UploadMedia(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def file_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> UploadType:
        raise NotImplementedError

    @abstractmethod
    async def read(self) -> bytes:
        raise NotImplementedError
