from typing import Self

from maxo.omit import Omittable, Omitted
from maxo.types.api.share_attachment_payload import ShareAttachmentPayload
from maxo.types.base import MaxoType
from maxo.types.enums.attachment_type import AttachmentType


class ShareAttachment(MaxoType):
    type = AttachmentType.SHARE

    payload: ShareAttachmentPayload = ShareAttachmentPayload()
    title: Omittable[str | None] = Omitted()
    description: Omittable[str | None] = Omitted()
    image_url: Omittable[str | None] = Omitted()

    @classmethod
    def factory(
        cls,
        url: Omittable[str | None] = Omitted(),
        token: Omittable[str | None] = Omitted(),
        title: Omittable[str | None] = Omitted(),
        description: Omittable[str | None] = Omitted(),
        image_url: Omittable[str | None] = Omitted(),
    ) -> Self:
        return cls(
            payload=ShareAttachmentPayload(
                url=url,
                token=token,
            ),
            title=title,
            description=description,
            image_url=image_url,
        )
