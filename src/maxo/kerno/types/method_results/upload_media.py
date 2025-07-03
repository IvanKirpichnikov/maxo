from collections.abc import Mapping

from maxo.kerno.types.base import MaxoType
from maxo.omit import Omittable, Omitted, is_defined


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
