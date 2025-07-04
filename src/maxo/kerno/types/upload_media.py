import io
import os
from abc import abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable

from anyio import open_file

from maxo.kerno.types.enums.upload_type import UploadType


@runtime_checkable
class UploadMedia(Protocol):
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

    @classmethod
    def from_image(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.IMAGE)

    @classmethod
    def from_video(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.VIDEO)

    @classmethod
    def from_audio(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.AUDIO)

    @classmethod
    def from_file(cls, data: bytes, file_name: str) -> "BufferedUploadMedia":
        return cls(data=data, file_name=file_name, type=UploadType.FILE)

    @property
    def type(self) -> UploadType:
        return self._type

    @property
    def file_name(self) -> str:
        return self._file_name

    async def read(self) -> bytes:
        return io.BytesIO(self._data).read()


class FSUploadMedia(UploadMedia):
    __slots__ = (
        "_file_name",
        "_path",
        "_type",
    )

    def __init__(
        self,
        path: str | Path,
        type: UploadType,
        file_name: str | None = None,
    ) -> None:
        if file_name is None:
            file_name = os.path.basename(path)  # noqa: PTH119

        self._path = path
        self._type = type
        self._file_name = file_name

    @classmethod
    def from_image(cls, path: str | Path, file_name: str | None = None) -> "FSUploadMedia":
        return cls(path=path, file_name=file_name, type=UploadType.IMAGE)

    @classmethod
    def from_video(cls, path: str | Path, file_name: str | None = None) -> "FSUploadMedia":
        return cls(path=path, file_name=file_name, type=UploadType.VIDEO)

    @classmethod
    def from_audio(cls, path: str | Path, file_name: str | None = None) -> "FSUploadMedia":
        return cls(path=path, file_name=file_name, type=UploadType.AUDIO)

    @classmethod
    def from_file(cls, path: str | Path, file_name: str | None = None) -> "FSUploadMedia":
        return cls(path=path, file_name=file_name, type=UploadType.FILE)

    @property
    def type(self) -> UploadType:
        return self._type

    @property
    def file_name(self) -> str:
        return self._file_name

    async def read(self) -> bytes:
        async with await open_file(self._path, "rb") as file:
            return await file.read()
