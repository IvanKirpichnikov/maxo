from collections.abc import Mapping

from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType


class UploadImagePhotoTokenResult(MaxoType):
    token: str


class UploadMediaResult(MaxoType):
    token: Omittable[str] = Omitted()
    photos: Omittable[Mapping[str, UploadImagePhotoTokenResult]] = Omitted()

    @property
    def last_token(self) -> str:
        if is_defined(self.token):
            return self.token
        if is_defined(self.photos):
            return list(self.photos.values())[-1].token
        raise RuntimeError
